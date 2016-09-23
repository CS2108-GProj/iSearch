import csv
from scipy import spatial
from Classifier import Classifier
from NodeLookup import NodeLookup

class Searcher:
    def __init__(self):
        self.index = {}
        self.indexFile = './index.csv'

    def preprocessIndex(self):
        with open(self.indexFile, 'rb') as csvfile:
            index_reader = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(index_reader):
                self.index[line[1008]] = map(lambda x: float(x), line[:1008])

    def search(self, feature):
        feature = map(lambda x: float(x), feature)
        self.preprocessIndex()
        res = []
        for image, imageFeature in self.index.iteritems():
            sim = 1 - spatial.distance.cosine(feature, imageFeature)
            res.append((image, sim))
        top5 = sorted(res, key=lambda tup: tup[1], reverse=True)[:5]
        print top5

if __name__ == '__main__':
    classify = Classifier()
    lookup = NodeLookup()
    feature = classify.run('../ImageData/test/data/antlers/0544_1000119801.jpg')
    top_k = feature.argsort()[-5:][::-1]
    for node_id in top_k:
      human_string = lookup.id_to_string(node_id)
      score = feature[node_id]
      print('%s (score = %.5f)' % (human_string, score))
    searcher = Searcher()
    searcher.search(feature)
