import argparse
import sys
import time

from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError

API_SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
API_VERSION = 'v1beta1'
DISCOVERY_API = 'https://cloudiot.googleapis.com/$discovery/rest'
SERVICE_NAME = 'cloudiot'


def discovery_url(api_key):
    """Construct the discovery url for the given api key."""
    return '{}?version={}&key={}'.format(DISCOVERY_API, API_VERSION, api_key)



class DeviceRegistry(object):
    """Administer a set of devices for a device registry."""

    def __init__(
            self, project_id, registry_id, cloud_region,
            service_account_json, api_key, pubsub_topic):
        """Lookup or create a device registry for the given project."""
        self.parent = 'projects/{}/locations/{}'.format(
                project_id, cloud_region)
        self.full_name = '{}/registries/{}'.format(self.parent, registry_id)
        credentials = service_account.Credentials.from_service_account_file(
                        service_account_json)
        scoped_credentials = credentials.with_scopes(API_SCOPES)

        if not credentials:
            sys.exit(
                    'Could not load service account credential from {}'
                    .format(service_account_json))

        self._service = discovery.build(
                SERVICE_NAME,
                API_VERSION,
                discoveryServiceUrl=discovery_url(api_key),
                credentials=scoped_credentials)

        # Lookup or create the device registry. Here we bind the registry to
        # the given Cloud Pub/Sub topic. All devices within a registry will
        # have their telemetry data published to this topic, using attributes
        # to indicate which device the data originated from.
        body = {
            'eventNotificationConfig': {
                'pubsubTopicName': pubsub_topic
            },
            'id': registry_id
        }
        request = self._service.projects().locations().registries().create(
            parent=self.parent, body=body)

        try:
            response = request.execute()
            print('Created registry', registry_id)
            print(response)
        except HttpError as e:
            if e.resp.status == 409:
                # Device registry already exists
                print(
                        'Registry', registry_id,
                        'already exists - looking it up instead.')
                request = self._service.projects().locations().registries(
                        ).get(name=self.full_name)
                request.execute()

            else:
                raise

    def delete(self):
        """Delete this registry."""
        request = self._service.projects().locations().registries().delete(
                name=self.full_name)
        return request.execute()

    def list_devices(self):
        """List all devices in the registry."""
        request = self._service.projects().locations().registries().devices(
                ).list(parent=self.full_name)
        response = request.execute()
        return response.get('devices', [])

    def _create_device(self, device_template):
        request = self._service.projects().locations().registries().devices(
        ).create(parent=self.full_name, body=device_template)
        return request.execute()

    def create_device_with_rs256(self, device_id, certificate_file):
        """Create a new device with the given id, using RS256 for
        authentication."""
        with open(certificate_file) as f:
            certificate = f.read()

        # Create a device with the given certificate. Note that you can have
        # multiple credentials associated with a device.
        device_template = {
            'id': device_id,
            'credentials': [{
                'publicKey': {
                    'format': 'RSA_X509_PEM',
                    'key': certificate
                }
            }]
        }
        return self._create_device(device_template)

    def create_device_with_es256(self, device_id, public_key_file):
        """Create a new device with the given id, using ES256 for
        authentication."""
        with open(public_key_file) as f:
            public_key = f.read()

        # Create a device with the given public key. Note that you can have
        # multiple credentials associated with a device.
        device_template = {
            'id': device_id,
            'credentials': [{
                'publicKey': {
                    'format': 'ES256_PEM',
                    'key': public_key
                }
            }]
        }
        return self._create_device(device_template)

    def create_device_with_no_auth(self, device_id):
        """Create a new device with no authentication."""
        device_template = {
            'id': device_id,
        }
        return self._create_device(device_template)

    def patch_es256_for_auth(self, device_id, public_key_file):
        """Patch the device to add an ES256 public key to the device."""
        with open(public_key_file) as f:
            public_key = f.read()

        patch = {
            'credentials': [{
                'publicKey': {
                    'format': 'ES256_PEM',
                    'key': public_key
                }
            }]
        }

        device_name = '{}/devices/{}'.format(self.full_name, device_id)

        # Patch requests use a FieldMask to determine which fields to update.
        # In this case, we're updating the device's credentials with a new
        # entry.
        request = self._service.projects().locations().registries().devices(
        ).patch(name=device_name, updateMask='credentials', body=patch)

        return request.execute()

    def delete_device(self, device_id):
        """Delete the device with the given id."""
        device_name = '{}/devices/{}'.format(self.full_name, device_id)
        request = self._service.projects().locations().registries().devices(
        ).delete(name=device_name)
        return request.execute()

def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
            description='Example of Google Cloud IoT Core device management.')
    # Required arguments
    parser.add_argument(
            '--project_id', required=True, help='GCP cloud project name.')
    parser.add_argument(
            '--pubsub_topic',
            required=True,
            help=('Google Cloud Pub/Sub topic. '
                  'Format is projects/project_id/topics/topic-id'))
    parser.add_argument('--api_key', required=True, help='Your API key.')

    # Optional arguments
    parser.add_argument(
            '--ec_public_key_file',
            default='ec_public.pem',
            help='Path to public ES256 key file.')
    parser.add_argument(
            '--rsa_certificate_file',
            default='rsa_cert.pem',
            help='Path to RS256 certificate file.')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--service_account_json',
            default='service_account.json',
            help='Path to service account json file.')
    parser.add_argument(
            '--registry_id',
            default=None,
            help='Registry id. If not set, a name will be generated.')

    return parser.parse_args()

def main():
    args = parse_command_line_args()

    # The example id for our registry.
    if args.registry_id is None:
        registry_id = 'cloudiot_device_manager_example_registry_{}'.format(
                int(time.time()))
    else:
        registry_id = args.registry_id

    # Lookup or create the registry.
    print 'Creating registry', registry_id, 'in project', args.project_id
    device_registry = DeviceRegistry(
            args.project_id, registry_id, args.cloud_region,
            args.service_account_json, args.api_key, args.pubsub_topic)

    # List devices for the (empty) registry
    print('Current devices in the registry:')
    for device in device_registry.list_devices():
        print device

    rs256_device_id = 'rs256-device'
    print('Creating RS256 authenticated device', rs256_device_id)
    device_registry.create_device_with_rs256(
            rs256_device_id, args.rsa_certificate_file)

if __name__ == '__main__':
    main()
