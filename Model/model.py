

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

# define variable types
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
FEATURES =  [c for c in COLUMNS if c not in LABEL]

FEATURE_COLUMNS = []
for f in FEATURES:
  # remove useless features
  if f not in ['SensorMeasure17', 'SensorMeasure10', 'SensorMeasure16', 'SensorMeasure1', 'OpSet3']:
    FEATURE_COLUMNS += [tf.contrib.layers.real_valued_column(f, normalizer=None)]


def build_estimator(model_dir, hidden_units=None):
  m = tf.contrib.learn.DNNRegressor(
    model_dir=model_dir, 
    enable_centered_bias=True,
    feature_columns=FEATURE_COLUMNS,
    hidden_units=hidden_units or [50,50])
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
      for column in FEATURE_COLUMNS
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
                      shuffle=False,
                      skip_header_lines=0,
                      batch_size=100):
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

  