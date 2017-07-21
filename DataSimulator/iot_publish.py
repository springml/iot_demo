import argparse
import datetime
import json
import time
import random
import jwt
import paho.mqtt.client as mqtt
import numpy as np
from create_device import DeviceRegistry
import collections

def create_jwt(project_id, private_key_file, algorithm):
	"""Create a JWT (https://jwt.io) to establish an MQTT connection."""
	token = {
		'iat': datetime.datetime.utcnow(),
		'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
		'aud': project_id
	}
	with open(private_key_file, 'r') as f:
		private_key = f.read()
		#print 'Creating JWT using {} from private key file {}'.format(
		#algorithm, private_key_file)
	return jwt.encode(token, private_key, algorithm=algorithm)
def error_str(rc):
	"""Convert a Paho error to a human readable string."""
  	return '{}: {}'.format(rc, mqtt.error_string(rc))

class Device(object):
	#Represents the state of a single device

	def __init__(self, device_id, unit, plant):
		
		self.connected = False
		self.features = ["OpSet1",  "OpSet2", "OpSet3", "SensorMeasure1", "SensorMeasure2", "SensorMeasure3", "SensorMeasure4", "SensorMeasure5", "SensorMeasure6", "SensorMeasure7", "SensorMeasure8", "SensorMeasure9", "SensorMeasure10", "SensorMeasure11", "SensorMeasure12", "SensorMeasure13", "SensorMeasure14", "SensorMeasure15", "SensorMeasure16", "SensorMeasure17", "SensorMeasure18", "SensorMeasure19", "SensorMeasure20", "SensorMeasure21"]
		self.device_id = device_id
		self.unit = plant["Units"][unit][0]
		self.IndustrialPlant = plant["Name"]
		self.latitude = plant["Latitude"]
		self.longitude = plant["Longtitude"]
		self.mqtt_telemetry_topic = '/devices/{}/events'.format(device_id)
		self.device_time = plant["Units"][unit][1]
		self.sensor_trends = {}

	def initialize_features(self):
		with open("feature_distribution.json") as fp:
			data = fp.read()
			text = data.encode('ascii', 'ignore')
		self.sensor_trends = json.loads(text)

	def update_sensor_data(self, cycle):
		"""Pretend to read the device's feature data."""
		sensor_reading = collections.OrderedDict()
		sensor_reading["IndustrialPlantName"] = self.IndustrialPlant
		sensor_reading["Latitude"] = self.latitude
		sensor_reading["Longtitude"] = self.longitude
		sensor_reading["UnitNumber"] = self.unit
		sensor_reading["Cycle"] = cycle
		for feature in self.features:
			sensor_reading[feature] = abs(np.random.normal(self.sensor_trends[feature + "_" + str(cycle) + "_" + "mean"], \
							self.sensor_trends[feature + "_" + str(cycle) + "_" + "std"] ))
		return json.dumps(sensor_reading)

	def dead_sensor_data(self, cycle):
		"""Pretend to read the device's feature data."""
		sensor_reading = collections.OrderedDict()
		sensor_reading["IndustrialPlantName"] = self.IndustrialPlant
		sensor_reading["Latitude"] = self.latitude
		sensor_reading["Longtitude"] = self.longitude
		sensor_reading["UnitNumber"] = self.unit
		sensor_reading["Cycle"] = 99999999
		for feature in self.features:
			sensor_reading[feature] = abs(np.random.normal(self.sensor_trends[feature + "_" + str(cycle) + "_" + "mean"], \
							self.sensor_trends[feature + "_" + str(cycle) + "_" + "std"] ))
		return json.dumps(sensor_reading)
	
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
		'--private_key_file', default='PemFiles/rsa_private.pem', help='Path to private key file.')
	parser.add_argument(
		'--pubsub_topic',
		required=True,
		help=('Google Cloud Pub/Sub topic. '
			'Format is projects/project_id/topics/topic-id'))
	parser.add_argument('--api_key', required=True, help='Your API key.')
	parser.add_argument(
		'--service_account_json',
		required=True,
		help='Path to service account json file.')
	parser.add_argument(
		'--plants_info_dir',
		default = 'OilRigInfo.json',
		help='Path to file about the various Industrial Plants')
	parser.add_argument(
		'--cloud_region', default='us-central1', help='GCP cloud region')
	parser.add_argument('--num_plants', default=2, help='Number of Industrial Plants to simulate', type=int)
	parser.add_argument(
		'--rsa_certificate_file',
		default='PemFiles/rsa_cert.pem',
		help='Path to RS256 certificate file.')
	parser.add_argument(
		'--ca_certs',
		default='PemFiles/roots.pem',
		help='CA root certificate. Get from https://pki.google.com/roots.pem')
	parser.add_argument(
		'--publish_latency',
		default=.08,
		help='Publish Latency'
		)

	return parser.parse_args()
def close_client(client):
	client.disconnect()
	client.loop_stop()

def setup_client_device(registry_id, device_id, unit, plant):
	'''Creates a client which is a connection over MQTT for a device to a pubsub topic. 
	   For each Device ID, creates a corresponding Device (Code Defined Class) which will simulate data for that particular Device ID 
	'''

	args = parse_command_line_args()
	
	device = Device(device_id, unit, plant)
	
	client = mqtt.Client(client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format( \
			args.project_id, args.cloud_region, registry_id, device_id))
	
	#setting a username and password for authenticating to Broker (IOT Core) creating a JWT singed with private key
	client.username_pw_set( username='unused', \
			password=create_jwt(args.project_id, args.private_key_file, 'RS256'))
	

	#configures network encryption and authentication
	client.tls_set(ca_certs=args.ca_certs)



	client.on_connect = device.on_connect
	client.on_publish = device.on_publish
	client.on_disconnect = device.on_disconnect
	client.on_subscribe = device.on_subscribe
	client.on_message = device.on_message
	
	client.connect('mqtt.googleapis.com', 8883)

	client.loop_start()

	# Wait up to 5 seconds for the device to connect.
	#device.wait_for_connection(5)
	device.initialize_features()

	return client, device
	
def get_plants_info(plants_info_dir, num_plants):
	'''
	Gets basic information (Name, Location, Units) on the Industrials Plants from a flat file specified in the command line.
	This function then returns the Json with the basic info.
	'''
	with open(plants_info_dir) as fp:
		data = fp.read()
		text = data.encode('ascii', 'ignore')
	plants_info = json.loads(text)
	return plants_info["plants"][:num_plants]

def main():
	args = parse_command_line_args()

	registry_id = 'cloudiot_device_manager_registry_18923213'
	#registry_id = 'cloudiot_device_manager_registry_{}'.format(int(time.time()))

	#Looking up already called registry based upon registry_id specified above
	device_registry = DeviceRegistry( \
		args.project_id, registry_id, args.cloud_region, \
		args.service_account_json, args.api_key, args.pubsub_topic)


	plants_info = get_plants_info(args.plants_info_dir, args.num_plants)

	Clients = []
	Devices = []

	#Looping through all the plants and their corresponding units within a plant to generate devices and clients 
	for plant in plants_info:
		for unit in xrange(len(plant["Units"])):
			device_id = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in xrange(10))
			device_registry.create_device_with_rs256(device_id, args.rsa_certificate_file)
			client, device = setup_client_device(registry_id, device_id, unit, plant)
			Clients.append(client)
			Devices.append(device)


	max_device_time = max([Devices[i].device_time for i in xrange(len(Devices))])
	

	#looping through the lifecycle of each device and publishing the measurements
	for cycle in xrange(1, max_device_time+2):

		for j in xrange(len(Devices)):
			
			if cycle > Devices[j].device_time:
				payload = Devices[j].dead_sensor_data(cycle)
				Clients[j].publish(Devices[j].mqtt_telemetry_topic, payload, qos=1)
				print payload
				time.sleep(float(args.publish_latency))
				continue

			payload = Devices[j].update_sensor_data(cycle)
			print payload

			Clients[j].publish(Devices[j].mqtt_telemetry_topic, payload, qos=1)
			time.sleep(float(args.publish_latency))

	print [(Devices[i].device_time, Devices[i].unit, Devices[i].IndustrialPlant) for i in xrange(len(Devices))]

	for client in Clients:
		close_client(client)
	
	

if __name__ == '__main__':
	main()






















