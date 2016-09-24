from sift_vw.match import Searcher as VW_Search
from color_histogram.match import Searcher as CH_Search

# Define constant string
IMAGE_NAME = 'image_name'
TOTAL_SCORE = 'total_score'
FEATURE_SCORE = 'feature_score'

CH_SCORE = 'CH_score'
VW_SCORE = 'VW_score'
VC_SCORE = 'VC_score'
NULL_NAME = 'NULL'

# Define ratio
CH_RATIO = -0.1
VW_RATIO = -0.1
VC_RATIO = 0.1

def search(query, CH=False, VW=False, VC=False, threshold=10):
    CH_result, VW_result, VC_result = get_null_score(threshold)

    if CH:
        CH_result = CH_Search.search(query_image=query, limit=threshold)

    if VW:
        VW_result = VW_Search.search(query_image=query, limit=threshold)

    if VC:
        pass
        #VC_result = VC_Search.serach(query_image=query, limit=threshold)

    integrated_score = get_integrate_score(CH_result, VW_result, VC_result)
    sorted_integrate_score = get_sorted_integrate_score(integrated_score)

    return sorted_integrate_score


# Merge sort total score
def get_sorted_integrate_score(integrated_score):
    unsorted_integrated_score = []

    images_keys = [key for key in integrated_score.keys() if key != NULL_NAME]
    for item_name in images_keys:
        total_score = CH_RATIO * integrated_score[item_name][CH_SCORE] + \
                        VW_RATIO * integrated_score[item_name][VW_SCORE] + \
                        VC_RATIO * integrated_score[item_name][VC_SCORE]

        unsorted_integrated_score.append({IMAGE_NAME: item_name, TOTAL_SCORE: total_score, FEATURE_SCORE: integrated_score[item_name]})

    return sorted(unsorted_integrated_score, key=lambda item_score: item_score[TOTAL_SCORE], reverse=True)


# Initialize integrated score panel
def get_initialized_integrate_score(CH_result, VW_result, VC_result):
    integrate_score_panel = {}

    for ch_item, vw_item, vc_item in zip(CH_result, VW_result, VC_result):
        ch_name = get_CH_name(ch_item)

        vw_name = get_VW_name(vw_item)

        vc_name = get_VC_name(vc_item)

        try:
            integrate_score_panel[ch_name]
        except KeyError:
            integrate_score_panel[ch_name] = {}
            integrate_score_panel[ch_name][CH_SCORE] = 0
            integrate_score_panel[ch_name][VW_SCORE] = 0
            integrate_score_panel[ch_name][VC_SCORE] = 0

        try:
            integrate_score_panel[vw_name]
        except KeyError:
            integrate_score_panel[vw_name] = {}
            integrate_score_panel[vw_name][CH_SCORE] = 0
            integrate_score_panel[vw_name][VW_SCORE] = 0
            integrate_score_panel[vw_name][VC_SCORE] = 0

        try:
            integrate_score_panel[vc_name]
        except KeyError:
            integrate_score_panel[vc_name] = {}
            integrate_score_panel[vc_name][CH_SCORE] = 0
            integrate_score_panel[vc_name][VW_SCORE] = 0
            integrate_score_panel[vc_name][VC_SCORE] = 0

    return integrate_score_panel


# Add scores to individual items
def get_integrate_score(CH_result, VW_result, VC_result):
    integrate_score_panel = get_initialized_integrate_score(CH_result, VW_result, VC_result)

    for ch_item, vw_item, vc_item in zip(CH_result, VW_result, VC_result):
        ch_name = get_CH_name(ch_item)
        ch_score = get_CH_score(ch_item)

        vw_name = get_VW_name(vw_item)
        vw_score = get_VW_score(vw_item)

        vc_name = get_VC_name(vc_item)
        vc_score = get_VC_score(vc_item)

        integrate_score_panel[ch_name][CH_SCORE] = ch_score
        integrate_score_panel[vw_name][VW_SCORE] = vw_score
        integrate_score_panel[vc_name][VC_SCORE] = vc_score

    return integrate_score_panel


def get_null_score(threshold):
    null_score_array = []
    for i in range(threshold):
        null_score_array.append((NULL_NAME, 0))
    return null_score_array


def get_CH_name(item):
    return item[1]


def get_CH_score(item):
    return item[0]


def get_VW_name(item):
    return item[0]


def get_VW_score(item):
    return item[1]


def get_VC_name(item):
    return item[0]


def get_VC_score(item):
    return item[1]


if __name__ == "__main__":
    ch = [(1, 'a'), (1, 'b'), (1, 'c')]
    vw = [('a', 1), ('c', 1), ('d', 1)]
    vc = get_null_score(3)

    print get_sorted_integrate_score(get_integrate_score(ch, vw, vc))
