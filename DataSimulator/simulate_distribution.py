import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import json
import math


def load_data():
	''' Takes Data from all csv files from CMAPPS dataset and loads into a dataframe'''

	allFiles = ["data/CMAPSSData/train_FD001.txt", "data/CMAPSSData/train_FD002.txt", "data/CMAPSSData/train_FD003.txt", "data/CMAPSSData/train_FD004.txt", \
            "data/CMAPSSData/test_FD001.txt", "data/CMAPSSData/test_FD002.txt", "data/CMAPSSData/test_FD003.txt", "data/CMAPSSData/test_FD004.txt"]
	file_suffixes = ["_train_FD001", "_train_FD002", "_train_FD003", "_train_FD004", "_test_FD001", "_test_FD002", \
               "_test_FD003", "_test_FD004"]
	all_dfs = []
	for i in xrange(len(allFiles)):
		temp_df = pd.read_csv(allFiles[i], header=None, sep = ' ', index_col=False)
		temp_df[0] =  temp_df[0].astype(str) + file_suffixes[i]
		all_dfs.append(temp_df)

	df = pd.concat(all_dfs, ignore_index=True)

	#changing column names to make them more human readable
	col_names = ["unit", "time", "operational_setting_1", "operational_setting_2", "operational_setting_3"]
	for i in xrange(1,24):
		col_names.append("sensor_measurement_" + str(i))
	df.columns = col_names
	df.drop(['sensor_measurement_22', "sensor_measurement_23"], axis=1, inplace=True)

	return df

def generate_distribution_file(df):

	np.set_printoptions(suppress=True)
	#group by functions to apply on all observational column in dataframe
	gb_functions = { 'operational_setting_1': ['mean', 'std'], 'operational_setting_2'  : ['mean', 'std'], 'operational_setting_3'  : ['mean', 'std'],  'sensor_measurement_1': ['mean', 'count', 'std'], 'sensor_measurement_2': ['mean', 'std'], 'sensor_measurement_3'  : ['mean', 'std'], 'sensor_measurement_4'  : ['mean', 'std'], \
	'sensor_measurement_5'  : ['mean', 'std'], 'sensor_measurement_6'  : ['mean', 'std'], 'sensor_measurement_7'  : ['mean', 'std'], 'sensor_measurement_8'  : ['mean', 'std'],  'sensor_measurement_9'  : ['mean', 'std'], 'sensor_measurement_10'  : ['mean', 'std'], 'sensor_measurement_11'  : ['mean', 'std'], 'sensor_measurement_12'  : ['mean', 'std'], \
	'sensor_measurement_13'  : ['mean', 'std'], 'sensor_measurement_14'  : ['mean', 'std'], 'sensor_measurement_15'  : ['mean', 'std'], 'sensor_measurement_16'  : ['mean', 'std'],  'sensor_measurement_17'  : ['mean', 'std'], 'sensor_measurement_18'  : ['mean', 'std'], 'sensor_measurement_19'  : ['mean', 'std'], 'sensor_measurement_20'  : ['mean', 'std'], 'sensor_measurement_21'  : ['mean', 'std']}

	features = df.columns[2:].tolist()

	df_trends = df.groupby(['time']).agg(gb_functions)

	feature_distribution = {}
	for time in xrange(1, len(df_trends)):
		for feature in features:
			std = df_trends[feature]["std"][time]
			if math.isnan(std):
				std = 10
			feature_distribution[feature + "_" + str(time) + "_" + "mean"] = df_trends[feature]["mean"][time]
			feature_distribution[feature + "_" + str(time) + "_" + "std"] = std
	with open("feature_distribution.json", 'w') as fp:
		json.dump(feature_distribution, fp)

if __name__ == '__main__':
	df = load_data()
	generate_distribution_file(df)
