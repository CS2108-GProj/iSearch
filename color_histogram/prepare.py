# USAGE
# python prepare.py --dataset dataset --index index.csv

# import the necessary packages
from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

def prepare_local(image_set_path, data_set_path):

    # initialize the color descriptor
    cd = ColorDescriptor((8, 12, 3))
    # open the output index file for writing
    output = open(data_set_path, "w")
    # use glob to grab the image paths and loop over them
    for imagePath in glob.glob(image_set_path + "/*.jpg"):
        # extract the image ID (i.e. the unique filename) from the image
        # path and load the image itself
        imageID = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)

        # describe the image
        features = cd.describe(image)

        # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imageID, ",".join(features)))

    # close the index file
    output.close()

if __name__ == "__main__":
    prepare_local(image_set_path='../dataset', data_set_path='ch.txt')