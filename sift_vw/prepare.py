import os
from utils.img_hash import EXTS
from utils.lsh import LSH_sift
from utils.img_sift import sift2

def prepare_local(data_path, f_func, h_func, p_out):
    with open(p_out, 'w') as f_out:
        for root, dirs, files in os.walk(data_path):
            for f in files:
                postfix = f.split('.')[-1]
                if postfix not in EXTS: continue
                full_path = os.path.join(root, f)
                try:
                    F = f_func(full_path)
                    for f in F:
                        f = list(f)
                        h = h_func(f)
                        f_out.write('%s\t%s\t%s\n' % (full_path, repr(f), repr(h)))
                except Exception, e:
                    print repr(e)
                    print full_path

if __name__ == "__main__":
    dataset = 'sample_dataset/ferrari'
    prepare_local(dataset, sift2, LSH_sift, 'sift_data/sample_ferrari_sift_lsh.txt')