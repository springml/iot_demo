import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import json
import math


def load_data():
	''' Takes Data from all csv files from CMAPPS dataset and loads into a dataframe'''

	df = pd.read_csv("data/CMAPSSData/train_FD001.txt", header=None, sep = ' ', index_col=False)

	#changing column names to make them more human readable
	col_names = ["unit", "time", "OpSet1", "OpSet2", "OpSet3"]
	for i in xrange(1,24):
		col_names.append("SensorMeasure" + str(i))
	df.columns = col_names
	df.drop(['SensorMeasure22', "SensorMeasure23"], axis=1, inplace=True)

	return df

def generate_distribution_file(df):

	#group by functions to apply on all observational column in dataframe
	gb_functions = { 'OpSet1': ['mean', 'std'], 'OpSet2'  : ['mean', 'std'], 'OpSet3'  : ['mean', 'std'],  'SensorMeasure1': ['mean', 'count', 'std'], 'SensorMeasure2': ['mean', 'std'], 'SensorMeasure3'  : ['mean', 'std'],  \
	'SensorMeasure5'  : ['mean', 'std'], 'SensorMeasure6'  : ['mean', 'std'], 'SensorMeasure7'  : ['mean', 'std'], 'SensorMeasure8'  : ['mean', 'std'], 'SensorMeasure10'  : ['mean', 'std'],  'SensorMeasure12'  : ['mean', 'std'], \
	'SensorMeasure13'  : ['mean', 'std'], 'SensorMeasure14'  : ['mean', 'std'], 'SensorMeasure15'  : ['mean', 'std'], 'SensorMeasure16'  : ['mean', 'std'],  'SensorMeasure17'  : ['mean', 'std'], 'SensorMeasure18'  : ['mean', 'std'], 'SensorMeasure19'  : ['mean', 'std'], 'SensorMeasure20'  : ['mean', 'std'], 'SensorMeasure21'  : ['mean', 'std']}

	features = df.columns[2:].tolist()
	features.remove('SensorMeasure4')
	features.remove('SensorMeasure9')
	features.remove('SensorMeasure11')

	df_trends = df.groupby(['time']).agg(gb_functions)

	feature_distribution = {}
	for time in xrange(1, len(df_trends)):
		for feature in features:
			std = df_trends[feature]["std"][time]
			if math.isnan(std) or std == 0:
				std = .01
			feature_distribution[feature + "_" + str(time) + "_" + "mean"] = df_trends[feature]["mean"][time]
			feature_distribution[feature + "_" + str(time) + "_" + "std"] = abs(std)
	with open("feature_distribution_demo.json", 'w') as fp:
		json.dump(feature_distribution, fp)

if __name__ == '__main__':
	df = load_data()
	generate_distribution_file(df)
