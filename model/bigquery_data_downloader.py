
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# You need to pip install google.cloud and pandas in your GC cloud shell terminal window everytime
# sudo pip install google.cloud
# sudo pip install pandas
# 
# Make a new directory to hold your data:
# mkdir data
#
# Replace the generic table name in the query with your own BigQuery table name where
# your device data is stored
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import time
import pandas as pd
import numpy as np
import argparse
from google.cloud import bigquery 

# set to pull 100000 rows of training/testing data - adjust as needed
QUERY = """
	SELECT Cycle, SensorMeasure1, SensorMeasure2, SensorMeasure3, SensorMeasure4, SensorMeasure5,
	SensorMeasure6, SensorMeasure7, SensorMeasure8, SensorMeasure9, SensorMeasure10, SensorMeasure11,
	SensorMeasure12, SensorMeasure13, SensorMeasure14, SensorMeasure15, SensorMeasure16, SensorMeasure17,
	SensorMeasure18, SensorMeasure19, SensorMeasure20, SensorMeasure21, OpSet1, OpSet2, OpSet3, RemainingOperationCycles
	FROM [TTT] LIMIT 100000
"""

# Input Arguments for command line operation
argparser = argparse.ArgumentParser()
argparser.add_argument(
    '--project',
    help='Google Cloud Platform project where the BigQuery data lives',
    required=True
)
argparser.add_argument(
    '--table',
    help='Table name in standard SQL format: dataset.table',
    default='advertising.taxi_rides',
    required=True
)

args = argparser.parse_args()
arguments = args.__dict__

QUERY = QUERY.replace('TTT', arguments['table'])

print("Reading from table " + arguments['table'] + " in project " + arguments['project'])

# point client to google project
bq_client = bigquery.Client(project=arguments['project'])

query = bq_client.run_sync_query(QUERY)
query.timeout_ms = 20000
query.use_query_cache = False
query.run()  # API request

# loop and retry under latency condition
job = query.job
job.reload()
retry_count = 0
while retry_count < 20 and job.state != u'DONE':
    time.sleep(1.5**retry_count)      
    retry_count += 1
    job.reload()    
 
rows = query.rows
print('Row count:', len(rows))
 
iot_features = pd.DataFrame(rows)
iot_features.columns = ['Cycle', 'SensorMeasure1', 'SensorMeasure2', 'SensorMeasure3', 'SensorMeasure4', 'SensorMeasure5',
	'SensorMeasure6', 'SensorMeasure7', 'SensorMeasure8', 'SensorMeasure9', 'SensorMeasure10', 'SensorMeasure11',
	'SensorMeasure12', 'SensorMeasure13', 'SensorMeasure14', 'SensorMeasure15', 'SensorMeasure16', 'SensorMeasure17',
	'SensorMeasure18', 'SensorMeasure19', 'SensorMeasure20', 'SensorMeasure21', 'OpSet1', 'OpSet2', 'OpSet3', 'RemainingOperationCycles']

# order features
iot_features = iot_features[['Cycle', 'SensorMeasure1', 'SensorMeasure2', 'SensorMeasure3', 'SensorMeasure4', 'SensorMeasure5',
	'SensorMeasure6', 'SensorMeasure7', 'SensorMeasure8', 'SensorMeasure9', 'SensorMeasure10', 'SensorMeasure11',
	'SensorMeasure12', 'SensorMeasure13', 'SensorMeasure14', 'SensorMeasure15', 'SensorMeasure16', 'SensorMeasure17',
	'SensorMeasure18', 'SensorMeasure19', 'SensorMeasure20', 'SensorMeasure21', 'OpSet1', 'OpSet2', 'OpSet3', 'RemainingOperationCycles']]

# mkdir data - or wherever your want your data
msk = np.random.rand(len(iot_features)) < 0.5
train_file = iot_features[msk]
eval_file = iot_features[~msk]

# data needs to be in increments of 100 to match batch size
train_file = train_file[0:int(np.floor(len(train_file) / 100) * 100)]
eval_file = eval_file[0:int(np.floor(len(eval_file) / 100) * 100)]

# save to data folder
train_file.to_csv('data/turbofan_data_train.csv', index=False,  header=False)
eval_file.to_csv('data/turbofan_data_val.csv', index=False, header=False)
 


 