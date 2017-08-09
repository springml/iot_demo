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
	col_names = ["unit", "time", "OpSet1", "OpSet2", "OpSet3"]
	for i in xrange(1,24):
		col_names.append("SensorMeasure" + str(i))
	df.columns = col_names
	df.drop(['SensorMeasure22', "SensorMeasure23"], axis=1, inplace=True)

	return df

def generate_distribution_file(df):

	#group by functions to apply on all observational column in dataframe
	gb_functions = { 'OpSet1': ['mean', 'std'], 'OpSet2'  : ['mean', 'std'], 'OpSet3'  : ['mean', 'std'],  'SensorMeasure1': ['mean', 'count', 'std'], 'SensorMeasure2': ['mean', 'std'], 'SensorMeasure3'  : ['mean', 'std'], 'SensorMeasure4'  : ['mean', 'std'], \
	'SensorMeasure5'  : ['mean', 'std'], 'SensorMeasure6'  : ['mean', 'std'], 'SensorMeasure7'  : ['mean', 'std'], 'SensorMeasure8'  : ['mean', 'std'],  'SensorMeasure9'  : ['mean', 'std'], 'SensorMeasure10'  : ['mean', 'std'], 'SensorMeasure11'  : ['mean', 'std'], 'SensorMeasure12'  : ['mean', 'std'], \
	'SensorMeasure13'  : ['mean', 'std'], 'SensorMeasure14'  : ['mean', 'std'], 'SensorMeasure15'  : ['mean', 'std'], 'SensorMeasure16'  : ['mean', 'std'],  'SensorMeasure17'  : ['mean', 'std'], 'SensorMeasure18'  : ['mean', 'std'], 'SensorMeasure19'  : ['mean', 'std'], 'SensorMeasure20'  : ['mean', 'std'], 'SensorMeasure21'  : ['mean', 'std']}

	features = df.columns[2:].tolist()

	df_trends = df.groupby(['time']).agg(gb_functions)

	feature_distribution = {}
	for time in xrange(1, len(df_trends)):
		for feature in features:
			std = df_trends[feature]["std"][time]
			if math.isnan(std):
				std = 10
			feature_distribution[feature + "_" + str(time) + "_" + "mean"] = df_trends[feature]["mean"][time]
			feature_distribution[feature + "_" + str(time) + "_" + "std"] = abs(std)
	with open("feature_distribution.json", 'w') as fp:
		json.dump(feature_distribution, fp)

if __name__ == '__main__':
	df = load_data()
	generate_distribution_file(df)
