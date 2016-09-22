import os
from utils.img_sift import sift2
from utils.lsh import LSH_sift
from utils.kmeans import eculidean_dist
from prepare import prepare_local

def load(pin, obj):
    for line in open(pin):
        path, f_str, code = line.strip().split('\t')
        f = eval(f_str)
        code = eval(code)
        if code not in obj:
            obj[code] = {} 
        if path not in obj[code]:
            obj[code][path] = []
        obj[code][path].append(f)

def match(img_dst, obj, f_func, h_func, d_func):
    F = f_func(img_dst)
    match_dict = {}
    for f in F:
        code = h_func(f)
        if code not in obj:
            continue
        for path in obj[code]:
            match_dict[path] = match_dict.get(path, 0) + 1.
    result_list = [(k, 1-v/len(F)) for k, v in match_dict.items()]
    sort_list = sorted(result_list, key=lambda d:d[1])
    return sort_list[:5]

def sift_query(query_img_path, dataset='sample_dataset/ferrari', dataset_sift_list='sift_data/sample_ferrari_sift_lsh.txt'):
    sift_index = {}
    if not os.path.exists(dataset_sift_list):
        prepare_local(dataset, sift2, LSH_sift, dataset_sift_list)
    load(dataset_sift_list, sift_index)
    return match(query_img_path, sift_index, sift2, LSH_sift, eculidean_dist)

if __name__ == "__main__":
    #setname = 'ferrari'
    query = 'query.jpg'
    #sift_index = {}
    #load('%s_sift_lsh.txt' % setname, sift_index)
    #sift_list = match(dst_thum, sift_index, sift2, LSH_sift, eculidean_dist)
    print sift_query(query)