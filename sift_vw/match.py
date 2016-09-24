import os
from utils.img_sift import sift2
from utils.lsh import LSH_sift
from utils.kmeans import eculidean_dist
from prepare import prepare_local

class Searcher:
    def __init__(self, image_set_path='sample_dataset/ferrari', data_set_path='sift_data/sample_ferrari_sift_lsh.txt'):
        # store our index path
        self.data_set_path = data_set_path
        self.image_set_path = image_set_path

        if not os.path.exists(image_set_path):
            prepare_local(image_set_path, sift2, LSH_sift, data_set_path)

    def load(self, pin, obj):
        for line in open(pin):
            path, f_str, code = line.strip().split('\t')
            f = eval(f_str)
            code = eval(code)
            if code not in obj:
                obj[code] = {}
            if path not in obj[code]:
                obj[code][path] = []
            obj[code][path].append(f)

    def match(self, img_dst, obj, f_func, h_func, threshold):
        F = f_func(img_dst)
        match_dict = {}
        for f in F:
            code = h_func(f)
            if code not in obj:
                continue
            for path in obj[code]:
                match_dict[path] = match_dict.get(path, 0) + 1.
        result_list = [(k, 1 - v / len(F)) for k, v in match_dict.items()]
        sort_list = sorted(result_list, key=lambda d: d[1])
        return sort_list[:threshold]

    def search(self, query_image, limit=10):
        sift_index = {}
        self.load(self.data_set_path, sift_index)
        return self.match(query_image, sift_index, sift2, LSH_sift, limit)

if __name__ == "__main__":
    #setname = 'ferrari'
    query = 'query.jpg'
    #sift_index = {}
    #load('%s_sift_lsh.txt' % setname, sift_index)
    #sift_list = match(dst_thum, sift_index, sift2, LSH_sift, eculidean_dist)
    print Searcher().search(query)