# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from glob import glob
import re
import sys
import tarfile

import numpy as np
import urllib
import tensorflow as tf

DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'


class Classifier:
    def __init__(self):
        self.model_dir = './imagenet'
        self.index_dir = './indexes'
        self.index_file = './index.csv'

    def create_graph(self):
        """Creates a graph from saved GraphDef file and returns a saver."""
        # Creates graph from saved graph_def.pb.
        with tf.gfile.FastGFile(os.path.join(
                self.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def run_inference_on_image(self, image):
        """Runs inference on an image.

        Args:
          image: Image file name.

        Returns:
          Nothing
        """
        if not tf.gfile.Exists(image):
            tf.logging.fatal('File does not exist %s', image)
        image_data = tf.gfile.FastGFile(image, 'rb').read()

        # Creates graph from saved GraphDef.
        self.create_graph()

        with tf.Session() as sess:
            # Some useful tensors:
            # 'softmax:0': A tensor containing the normalized prediction across
            #   1000 labels.
            # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
            #   float description of the image.
            # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
            #   encoding of the image.
            # Runs the softmax tensor by feeding the image_data as input to the graph.
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)
            return predictions # 1008-D features

            # Creates node ID --> English string lookup.
            # node_lookup = NodeLookup()
            # top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
            # for node_id in top_k:
            #   human_string = node_lookup.id_to_string(node_id)
            #   score = predictions[node_id]
            #   print('%s (score = %.5f)' % (human_string, score))

    def maybe_download_and_extract(self):
        """Download and extract model tar file."""
        dest_directory = self.model_dir
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)
        filename = DATA_URL.split('/')[-1]
        filepath = os.path.join(dest_directory, filename)
        if not os.path.exists(filepath):
            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' % (
                    filename, float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()

            filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
            print()
            statinfo = os.stat(filepath)
            print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)

    def downloadAndGenerateIndex(self):
        self.maybe_download_and_extract()
        result = [y for x in os.walk('../ImageData/train/data') for y in glob(os.path.join(x[0], '*.jpg'))]
        images = set()
        duplicate = []
        for image in result:
            # avoid duplicate
            if os.path.isfile(image):
                base = os.path.basename(image)
                fileName = os.path.splitext(base)[0]
                if fileName in images:
                    duplicate.append(image)
                else:
                    images.add(fileName)
                continue
            with tf.Graph().as_default():
                self.run_inference_on_image(image)

    def run(self, image):
        return self.run_inference_on_image(image)
