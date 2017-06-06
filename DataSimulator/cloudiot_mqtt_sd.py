import argparse
import datetime
import json
import time
import random
import jwt
import paho.mqtt.client as mqtt
import numpy as np

def create_jwt(project_id, private_key_file, algorithm):
	"""Create a JWT (https://jwt.io) to establish an MQTT connection."""
	token = {
		'iat': datetime.datetime.utcnow(),
		'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
		'aud': project_id
	}
	with open(private_key_file, 'r') as f:
		private_key = f.read()
		print 'Creating JWT using {} from private key file {}'.format(
		algorithm, private_key_file)
	return jwt.encode(token, private_key, algorithm=algorithm)
def error_str(rc):
	"""Convert a Paho error to a human readable string."""
  	return '{}: {}'.format(rc, mqtt.error_string(rc))

class Device(object):
	#Represents the state of a single device

	def __init__(self, device_id):
		
		self.connected = False
		self.features = ["operational_setting_1",  "operational_setting_2", "operational_setting_3", "sensor_measurement_1", "sensor_measurement_2", "sensor_measurement_3", "sensor_measurement_4", "sensor_measurement_5", "sensor_measurement_6", "sensor_measurement_7", "sensor_measurement_8", "sensor_measurement_9", "sensor_measurement_10", "sensor_measurement_11", "sensor_measurement_12", "sensor_measurement_13", "sensor_measurement_14", "sensor_measurement_15", "sensor_measurement_16", "sensor_measurement_17", "sensor_measurement_18", "sensor_measurement_19", "sensor_measurement_20", "sensor_measurement_21"]
		self.device_id = device_id
		self.feature_trends = {}

	def initialize_features(self):
		with open("feature_distribution.json") as fp:
			data = fp.read()
			text = data.encode('ascii', 'ignore')
		self.feature_trends = json.loads(text)

	def update_feature_data(self, time):
		"""Pretend to read the device's feature data."""
		values = {}
		values["device_id"] = self.device_id
		values["time"] = time
		for feature in self.features:
			values[feature] = np.random.normal(self.feature_trends[feature + "_" + str(time) + "_" + "mean"], \
							self.feature_trends[feature + "_" + str(time) + "_" + "std"] )
		return json.dumps(values)

	def wait_for_connection(self, timeout):
		"""Wait for the device to become connected."""
		total_time = 0
		while not self.connected and total_time < timeout:
			time.sleep(1)
			total_time += 1

		if not self.connected:
			raise RuntimeError('Could not connect to MQTT bridge.')

	def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
		"""Callback for when a device connects."""
		print 'Connection Result:', error_str(rc)
		self.connected = True

	def on_disconnect(self, unused_client, unused_userdata, rc):
		"""Callback for when a device disconnects."""
		print 'Disconnected:', error_str(rc)
		self.connected = False

	def on_publish(self, unused_client, unused_userdata, unused_mid):
		"""Callback when the device receives a PUBACK from the MQTT bridge."""
		print 'Published message acked.'

	def on_subscribe(self, unused_client, unused_userdata, unused_mid,
		           granted_qos):
		"""Callback when the device receives a SUBACK from the MQTT bridge."""
		print 'Subscribed: ', granted_qos
		if granted_qos[0] == 128:
			print 'Subscription failed.'
	def on_message(self, unused_client, unused_userdata, message):
		"""Callback when the device receives a message on a subscription."""
		payload = str(message.payload)
		print "Received message '{}' on topic '{}' with Qos {}".format(
		payload, message.topic, str(message.qos))

		# The device will receive its latest config when it subscribes to the config
		# topic. If there is no configuration for the device, the device will
		# receive an config with an empty payload.
		if not payload:
			return

		# The config is passed in the payload of the message. In this example, the
		# server sends a serialized JSON string.
		data = json.loads(payload)
		if data['fan_on'] != self.fan_on:
			# If we're changing the state of the fan, print a message and update our
			# internal state.
			self.fan_on = data['fan_on']
		if self.fan_on:
			print 'Fan turned on.'
		else:
			print 'Fan turned off.'



def parse_command_line_args():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(
		description='Example Google Cloud IoT MQTT device connection code.')
	parser.add_argument(
		'--project_id', required=True, help='GCP cloud project name')
	parser.add_argument(
		'--registry_id', required=True, help='Cloud IoT registry id')
	parser.add_argument('--device_id', required=True, help='Cloud IoT device id')
	parser.add_argument(
		'--private_key_file', required=True, help='Path to private key file.')
	parser.add_argument(
		'--algorithm',
		choices=('RS256', 'ES256'),
		required=True,
		help='Which encryption algorithm to use to generate the JWT.')
	parser.add_argument(
		'--cloud_region', default='us-central1', help='GCP cloud region')
	parser.add_argument(
		'--ca_certs',
		default='roots.pem',
		help='CA root certificate. Get from https://pki.google.com/roots.pem')
	parser.add_argument(
		'--num_messages',
		type=int,
		default=100,
		help='Number of messages to publish.')
	parser.add_argument(
		'--mqtt_bridge_hostname',
		default='mqtt.googleapis.com',
		help='MQTT bridge hostname.')
	parser.add_argument(
		'--mqtt_bridge_port', default=8883, help='MQTT bridge port.')

	return parser.parse_args()

def main():
	args = parse_command_line_args()

	# Create our MQTT client and connect to Cloud IoT.
	client = mqtt.Client(
		client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
		args.project_id, args.cloud_region, args.registry_id, args.device_id))
	

	#setting a username and password for authenticating to Broker (IOT Core) creating a JWT singed with private key
	client.username_pw_set(
		username='unused',
		password=create_jwt(args.project_id, args.private_key_file,
			args.algorithm))
	
	#configures network encryption and authentication
	client.tls_set(ca_certs=args.ca_certs)

	device = Device(args.device_id)

	client.on_connect = device.on_connect
	client.on_publish = device.on_publish
	client.on_disconnect = device.on_disconnect
	client.on_subscribe = device.on_subscribe
	client.on_message = device.on_message

	client.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)

	client.loop_start()

	# This is the topic that the device will publish telemetry events (feature Data) to
	mqtt_telemetry_topic = '/devices/{}/events'.format(args.device_id)

	# This is the topic that the device will receive configuration updates on.
	#mqtt_config_topic = '/devices/{}/config'.format(args.device_id)

	# Wait up to 5 seconds for the device to connect.
	device.wait_for_connection(5)

	# Subscribe to the config topic.
	#client.subscribe(mqtt_config_topic, qos=1)
	device.initialize_features()
	
	device_time = int(np.random.normal(187.32, 82.40) + 1)
	
	for i in xrange(1, device_time):
		payload = device.update_feature_data(i)
		print 'Publishing payload', payload
		client.publish(mqtt_telemetry_topic, payload, qos=1)
		
		#demo how chaning values here breaks the transport
		time.sleep(.1)

	print device_time
	client.disconnect()
	client.loop_stop()

if __name__ == '__main__':
	main()






















