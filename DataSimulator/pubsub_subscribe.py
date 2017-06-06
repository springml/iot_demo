import time
import random
import pandas as pd 
from google.cloud import pubsub


def receive_message():
	pubsub_client = pubsub.Client()
	topic = pubsub_client.topic("hemanth_iot_test")
	subscription = topic.subscription("hemanth_subscription_iot_test")
	
	result = subscription.pull(return_immediately=True)
	count = 0
	while len(result) > 0:
		#print('Received {} messages.'.format(len(result)))
		#print result[0][1].data
		[ack_id for ack_id, message in result]
		subscription.acknowledge([ack_id for ack_id, message in result])
		result = subscription.pull(return_immediately=True)
		count = count + 1
	print count 
if __name__ == '__main__':
	receive_message()