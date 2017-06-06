from create_device import DeviceRegistry
import argparse

def parse_command_line_args():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(
		description='Example Google Cloud IoT MQTT device connection code.')
	parser.add_argument(
		'--project_id', required=True, help='GCP cloud project name')	
	parser.add_argument(
		'--registry_id',
		required = True,
		help='Registry id. If not set, a name will be generated.')

	parser.add_argument(
		'--cloud_region', default='us-central1', help='GCP cloud region')

	parser.add_argument(
		'--service_account_json',
		required=True,
		help='Path to service account json file.')
	parser.add_argument('--api_key', required=True, help='Your API key.')
	
	parser.add_argument(
		'--pubsub_topic',
		required=True,
		help=('Google Cloud Pub/Sub topic. '
			'Format is projects/project_id/topics/topic-id'))

	return parser.parse_args()

def main():

	args = parse_command_line_args()
	
	for registry in args.registry_id.split(','):
		#looking up registry
		device_registry = DeviceRegistry(
			args.project_id, registry, args.cloud_region,
			args.service_account_json, args.api_key, args.pubsub_topic)

		print len(device_registry.list_devices())

		for device in device_registry.list_devices():
			print device["id"] 
			
			device_registry.delete_device(device["id"])
			print "Deleting Device {}".format(device["id"])

		print len(device_registry.list_devices())
		device_registry.delete()

		print "Deleted Registry {}".format(args.registry_id)


if __name__ == '__main__':
	main()