import time
import os

if __name__ == '__main__':
	while True: 
		os.system("python iot_publish.py --project_id=mlpdm-168115  --pubsub_topic=projects/mlpdm-168115/topics/iot_mlpdm --api_key=AIzaSyAp1rmf0j9aIKBcoxa8KbHxjEgdcs_I_zs --service_account_json=PemFiles/mlpdm-3817c89891ab.json --plants_info_dir=OilRigInfo2.json --num_plants=2 --publish_latency=.3 --iot_registry=cloudiot_device_manager_registry_1892321")
		print "Pausing for 10 minutes between scripts"
		time.sleep(600)