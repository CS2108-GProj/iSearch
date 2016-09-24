# USAGE
# python prepare.py --dataset dataset --index index.csv

# import the necessary packages
import os
from glob import glob
from colordescriptor import ColorDescriptor
import cv2

def prepare_local(image_set_path, data_set_path):

    # initialize the color descriptor
    cd = ColorDescriptor((8, 12, 3))
    # open the output index file for writing
    output = open(data_set_path, "w")
    # use glob to grab the image paths and loop over them
    paths = [y for x in os.walk(image_set_path) for y in glob(os.path.join(x[0], '*.jpg'))]
    for imagePath in paths:
        # extract the image ID (i.e. the unique filename) from the image
        # path and load the image itself
        imageID = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)

        # describe the image
        features = cd.describe(image)

        # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imagePath, ",".join(features)))

    # close the index file
    output.close()

if __name__ == "__main__":
    prepare_local(image_set_path='../ImageData/train/data', data_set_path='ch.txt')