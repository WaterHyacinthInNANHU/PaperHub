import scraps.dblpSearcher as db
import htmlBuilder as hb
import os
import webbrowser
from config import settings
import copy
from utils.path import slugify

# load parameters
PUBLISHERS = settings['publishers']
NUMBER_PER_PUBLISHER = int(settings['number_per_publisher'])
NUMBER_PER_SEARCH = int(settings['number_per_search'])



def get_saving_path(name):
    abs_path = 'output/{}.html'.format(name)
    abs_path = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), abs_path)
    abs_path = abs_path.replace('\\', '/')
    return abs_path

# print(SAVE_FULL_PATH)
# target = "file:///{}".format(SAVE_FULL_PATH)


def search(terms):
    # terms = input("Search for: ")
    info_ = None
    while True:
        m = input("Search by publishers? [y/n]:")
        if m == 'y':
            info_ = db.search_by_conference(terms, PUBLISHERS, NUMBER_PER_PUBLISHER)
            break
        elif m == 'n':
            info_ = db.search(terms, NUMBER_PER_SEARCH)
            break
        else:
            continue
    return info_


def merge_info(info1, info2):
    info_ = copy.deepcopy(info1)
    # get existed titles in info1
    existed_titles = set()
    for item in info1:
        existed_titles.add(item['title'])
    # append unseen info2 items to info1
    for item in info2:
        title = item['title']
        if title not in existed_titles:
            info_.append(item)
            existed_titles.add(title)

    return info_


# search
while True:
    terms = [input("Search for: ")]
    info = search(terms[-1])
    while True:
        mode = input("Continue searching for other terms? [y/n]:")
        if mode == 'y':
            terms.append(input("Search for: "))
            info = merge_info(info, search(terms[-1]))
        elif mode == 'n':
            break
        else:
            continue

    info = db.sort_by_year(info)
    save_path = get_saving_path(slugify(terms))
    hb.save_as_html(info, save_path, heading=str(terms))
    webbrowser.open('file://' + save_path)

