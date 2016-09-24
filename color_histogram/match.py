# import the necessary packages
import os
from colordescriptor import ColorDescriptor
import cv2
import numpy as np
import csv
import prepare

class Searcher:
    def __init__(self, image_set_path='../dataset', data_set_path='ch.txt'):
        # store our index path
        self.data_set_path = data_set_path
        self.image_set_path = image_set_path

        if not os.path.exists(data_set_path):
            prepare.prepare_local(image_set_path=image_set_path, data_set_path=data_set_path)


    def search(self, query_image, limit = 10):
        # initialize our dictionary of results
        cd = ColorDescriptor((8, 12, 3))

        # load the query image and describe it
        img_file = cv2.imread(query_image)
        query = cd.describe(img_file)

        results = {}

        # open the index file for reading
        with open(self.data_set_path) as f:
            # initialize the CSV reader
            reader = csv.reader(f)

            # loop over the rows in the index
            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                # and our query features
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, query)

                # now that we have the distance between the two feature
                # vectors, we can udpate the results dictionary -- the
                # key is the current image ID in the index and the
                # value is the distance we just computed, representing
                # how 'similar' the image in the index is to our query
                results[row[0]] = d

            # close the reader
            f.close()

        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        results = sorted([(k, v) for (k, v) in results.items()])

        # return our (limited) results
        return results[:limit]

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d

if __name__ == "__main__":
    sample_query = '../ImageData/test/data/dog/0324_161473185.jpg'
    print Searcher().search(sample_query)