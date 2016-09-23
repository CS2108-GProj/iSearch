from sift_vw.match import Searcher as VW_Search
from color_histogram.match import Searcher as CH_Search

DEFAULT_IMAGE_LIST = 'pseudo_data.txt'

def get_default_data():
    return DEFAULT_IMAGE_LIST

def search(query, VC=False, CH=False, VW=False, threshold=10):
    data_result = get_default_data()
    #if VC:
        #data_result = VC_search(query, threshold=100)

    if CH:
        data_result = CH_Search().search(query, threshold=50)

    if VW:
        data_result = VW_Search().search(query, threshold=20)

    return data_result[:threshold]