

# Copyright 2016 Google Inc. All Rights Reserved. Licensed under the Apache
# License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""Define a Wide + Deep model for classification on structured data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import multiprocessing

import tensorflow as tf
from tensorflow.contrib import layers
from tensorflow.contrib.learn.python.learn.utils import input_fn_utils

tf.logging.set_verbosity(tf.logging.INFO)

# 1,2,0.0019,-0.0003,100.0,518.67,642.15,1591.82,1403.14,14.62,21.61,553.75,2388.04,9044.07,1.3,47.49,522.28,2388.07,8131.49,8.4318,0.03,392,2388,100.0,39.0,23.4236,190

# Define the initial ingestion of each feature used by your model.
# Additionally, provide metadata about the feature.
 
INPUT_COLUMNS = [
  # Continuous base columns for training/eval
  layers.real_valued_column('Cycle'),
  layers.real_valued_column('OpSet1'),
  layers.real_valued_column('OpSet2'),
  layers.real_valued_column('OpSet3'),
  layers.real_valued_column('SensorMeasure1'),
  layers.real_valued_column('SensorMeasure2'),
  layers.real_valued_column('SensorMeasure3'),
  layers.real_valued_column('SensorMeasure4'),
  layers.real_valued_column('SensorMeasure5'),
  layers.real_valued_column('SensorMeasure6'),
  layers.real_valued_column('SensorMeasure7'),
  layers.real_valued_column('SensorMeasure8'),
  layers.real_valued_column('SensorMeasure9'),
  layers.real_valued_column('SensorMeasure10'),
  layers.real_valued_column('SensorMeasure11'),
  layers.real_valued_column('SensorMeasure12'),
  layers.real_valued_column('SensorMeasure13'),
  layers.real_valued_column('SensorMeasure14'),
  layers.real_valued_column('SensorMeasure15'),
  layers.real_valued_column('SensorMeasure16'),
  layers.real_valued_column('SensorMeasure17'),
  layers.real_valued_column('SensorMeasure18'),
  layers.real_valued_column('SensorMeasure19'),
  layers.real_valued_column('SensorMeasure20'),
  layers.real_valued_column('SensorMeasure21'),
]



UNUSED_COLUMNS = ['UnitNumber']
CSV_COLUMN_DEFAULTS = [[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],
                        [0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],
                        [0.0],[0.0],[0.0],[0.0],[0.0],[0.0]]
 

COLUMNS = ['Cycle',
             'OpSet1',
             'OpSet2',
             'OpSet3',
             'SensorMeasure1',
             'SensorMeasure2',
             'SensorMeasure3',
             'SensorMeasure4',
             'SensorMeasure5',
             'SensorMeasure6',
             'SensorMeasure7',
             'SensorMeasure8',
             'SensorMeasure9',
             'SensorMeasure10',
             'SensorMeasure11',
             'SensorMeasure12',
             'SensorMeasure13',
             'SensorMeasure14',
             'SensorMeasure15',
             'SensorMeasure16',
             'SensorMeasure17',
             'SensorMeasure18',
             'SensorMeasure19',
             'SensorMeasure20',
             'SensorMeasure21',
             'RemainingUsefulLife']
 
LABEL = "RemainingUsefulLife"

def build_estimator(model_dir, hidden_units=None):
  ( Cycle ,
              OpSet1 ,
              OpSet2 ,
              OpSet3 ,
              SensorMeasure1 ,
              SensorMeasure2 ,
              SensorMeasure3 ,
              SensorMeasure4 ,
              SensorMeasure5 ,
              SensorMeasure6 ,
              SensorMeasure7 ,
              SensorMeasure8 ,
              SensorMeasure9 ,
              SensorMeasure10 ,
              SensorMeasure11 ,
              SensorMeasure12 ,
              SensorMeasure13 ,
              SensorMeasure14 ,
              SensorMeasure15 ,
              SensorMeasure16 ,
              SensorMeasure17 ,
              SensorMeasure18 ,
              SensorMeasure19 ,
              SensorMeasure20 ,
              SensorMeasure21 ) = INPUT_COLUMNS
  
  deep_columns = [
    Cycle ,
              OpSet1 ,
              OpSet2 ,
              OpSet3 ,
              SensorMeasure1 ,
              SensorMeasure2 ,
              SensorMeasure3 ,
              SensorMeasure4 ,
              SensorMeasure5 ,
              SensorMeasure6 ,
              SensorMeasure7 ,
              SensorMeasure8 ,
              SensorMeasure9 ,
              SensorMeasure10 ,
              SensorMeasure11 ,
              SensorMeasure12 ,
              SensorMeasure13 ,
              SensorMeasure14 ,
              SensorMeasure15 ,
              SensorMeasure16 ,
              SensorMeasure17 ,
              SensorMeasure18 ,
              SensorMeasure19 ,
              SensorMeasure20 ,
              SensorMeasure21
  ]

  m = tf.contrib.learn.DNNRegressor(
    model_dir=model_dir, 
    feature_columns=deep_columns,
    hidden_units=hidden_units or [100, 100])
  return m
 

def serving_input_fn():
  """Builds the input subgraph for prediction.
  This serving_input_fn accepts raw Tensors inputs which will be fed to the
  server as JSON dictionaries. The values in the JSON dictionary will be
  converted to Tensors of the appropriate type.
  Returns:
     tf.contrib.learn.input_fn_utils.InputFnOps, a named tuple
     (features, labels, inputs) where features is a dict of features to be
     passed to the Estimator, labels is always None for prediction, and
     inputs is a dictionary of inputs that the prediction server should expect
     from the user.
  """
 

  feature_placeholders = {
      column.name: tf.placeholder(column.dtype, [None])
      for column in INPUT_COLUMNS
  }
  features = {
      key: tf.expand_dims(tensor, -1)
      for key, tensor in feature_placeholders.items()
    }
 
  return input_fn_utils.InputFnOps(
    features,
    None,
    feature_placeholders
  )
 
def generate_input_fn(filenames,
                      num_epochs=None,
                      shuffle=True,
                      skip_header_lines=0,
                      batch_size=25):
  """Generates an input function for training or evaluation.
      Args:
          filenames: [str] list of CSV files to read data from.
          num_epochs: int how many times through to read the data.
            If None will loop through data indefinitely
          shuffle: bool, whether or not to randomize the order of data.
            Controls randomization of both file order and line order within
            files.
          skip_header_lines: int set to non-zero in order to skip header lines
            in CSV files.
          batch_size: int First dimension size of the Tensors returned by
            input_fn
      Returns:
          A function () -> (features, indices) where features is a dictionary of
            Tensors, and indices is a single Tensor of label indices.
  """

  def _input_fn():
    files = tf.concat([
        tf.train.match_filenames_once(filename)
        for filename in filenames
      ], axis=0)

    filename_queue = tf.train.string_input_producer(
      files, num_epochs=num_epochs, shuffle=shuffle)
    reader = tf.TextLineReader(skip_header_lines=skip_header_lines)

    _, rows = reader.read_up_to(filename_queue, num_records=batch_size)

    row_columns = tf.expand_dims(rows, -1)
    columns = tf.decode_csv(row_columns, record_defaults=CSV_COLUMN_DEFAULTS)
    features = dict(zip(COLUMNS, columns))

    RemainingUsefulLife = features[LABEL]
    features.pop(LABEL, 'no need of label in feature set')

    for col in UNUSED_COLUMNS:
      features.pop(col)


    if shuffle:
      # This operation maintains a buffer of Tensors so that inputs are
      # well shuffled even between batches.
      features = tf.train.shuffle_batch(
          features,
          batch_size,
          capacity=batch_size * 10,
          min_after_dequeue=batch_size*2 + 1,
          num_threads=multiprocessing.cpu_count(),
          enqueue_many=True,
          allow_smaller_final_batch=True
      )

    
    return features, RemainingUsefulLife
  return _input_fn

 
'''

gcloud ml-engine local train \
    --module-name predictivemaintenance.task \
    --package-path predictivemaintenance/ \
    -- \
    --train-file predictivemaintenance/data/turbofan_data_train.csv \
    --eval-file predictivemaintenance/data/turbofan_data_val.csv \
    --train-steps 500 \
    --job-dir predictivemaintenance/output
 
# python -m tensorflow.tensorboard --logdir=predictivemaintenance/output --port=8080
# http://localhost:8080/

https://console.cloud.google.com/storage/browser?project=mlpdm-168115

export PROJECT_ID=mlpdm-168115
export JOB_NAME=train_${USER}_$(date +%Y%m%d_%H%M%S)
export BUCKET=gs://pdmdemo
export TRAIN_PATH=${BUCKET}/jobs/${JOB_NAME}


gcloud ml-engine jobs submit training ${JOB_NAME} --job-dir ${TRAIN_PATH}/models/ --runtime-version 1.0 \
 --package-path=predictivemaintenance --module-name=predictivemaintenance.task \
 --staging-bucket=${BUCKET} --region=us-central1 -- --train-file ${BUCKET}/predictivemaintenance/data/turbofan_data_train.csv \
 --eval-file {BUCKET}/predictivemaintenance/data/turbofan_data_val.csv --train-steps 5000

 
models -> create
pdmdemo/jobs/train_manuel_amunategui_20170602_132023/models/export/Servo/1496437905348/

 
gcloud ml-engine predict --model predictivemaintenance_v2 --version v3 --json-instances data/test1.json

{"RemainingUsefulLife": 131, "SensorMeasure21": 23.363, "SensorMeasure20": 38.89, "SensorMeasure8": 2388.11, "SensorMeasure9": 9050.58, "SensorMeasure4": 1405.52, "SensorMeasure5": 14.62, "SensorMeasure6": 21.61, "SensorMeasure7": 554.09, "SensorMeasure1": 518.67, "SensorMeasure2": 642.1, "SensorMeasure3": 1583.55, "OpSet3": 100, "OpSet2": 0.0005, "OpSet1": 0.0004, "SensorMeasure16": 0.03, "SensorMeasure17": 391, "SensorMeasure14": 8131.66, "SensorMeasure15": 8.4264, "SensorMeasure12": 522.34, "SensorMeasure13": 2388.09, "SensorMeasure10": 1.3, "SensorMeasure11": 47.31, "SensorMeasure18": 2388, "SensorMeasure19": 100.0, "UnitNumber": 1, "Cycle": 61}
RemainingUsefulLife": 131
OUTPUTS
142.339


TRAINER_PACKAGE_PATH="/home/manuel_amunategui/predictivemaintenance"
now=$(date +"%Y%m%d_%H%M%S")
JOB_NAME="predmaint_$now"
MAIN_TRAINER_MODULE="predictivemaintenance.task"
JOB_DIR="gs://mlpdm/pdmdemo/predictivemaintenance"
PACKAGE_STAGING_LOCATION="gs://mlpdm/pdmdemo/predictivemaintenance/staging"
REGION="us-central1"
RUNTIME_VERSION="1.0"

GCS_PATH = "gs://mlpdm/pdmdemo/predictivemaintenance"
MODEL_NAME=predictivemaintenance  
VERSION_NAME=v1   
gcloud ml-engine models create ${MODEL_NAME} \
  --regions us-central1
gcloud ml-engine versions create \
  --origin 'gs://mlpdm/pdmdemo/predictivemaintenance/training/model/' \
  --staging-bucket 'gs://mlpdm/pdmdemo/predictivemaintenance/' \
  --model ${MODEL_NAME} \
  ${VERSION_NAME}
gcloud ml-engine versions set-default --model ${MODEL_NAME} ${VERSION_NAME}


gcloud ml-engine models create ${MODEL_NAME} \
  --regions us-central1
DEPLOYMENT_SOURCE="gs://mlpdm/pdmdemo/predictivemaintenance/"
MODEL_NAME=predictivemaintenance  
VERSION_NAME=v1  
gcloud ml-engine versions create ${VERSION_NAME} \
    --model ${MODEL_NAME} --origin $DEPLOYMENT_SOURCE

gcloud ml-engine predict --model predictivemaintenance_v3 --version v3 --json-instances data/test1.json


gcloud ml-engine local train \
    --module-name predictivemaintenance.task \
    --package-path predictivemaintenance/ \
    -- \
    --train-file predictivemaintenance/data/turbofan_data_train.csv \
    --eval-file predictivemaintenance/data/turbofan_data_val.csv \
    --train-steps 500 \
    --job-dir predictivemaintenance/output

# gcloud components update
gcloud ml-engine local predict --model-dir predictivemaintenance/output  --json-instances data/test1.json

'''
