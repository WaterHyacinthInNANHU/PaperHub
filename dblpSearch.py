import scraps.dblpSearcher as db
import html_builder as hbuild
import os
import webbrowser
from config import settings

# load parameters
PUBLISHERS = settings['publishers']
NUMBER_PER_PUBLISHER = int(settings['number_per_publisher'])
NUMBER_PER_SEARCH = int(settings['number_per_search'])

# init output file
SAVE_PATH = 'output/dblp_output.html'
SAVE_FULL_PATH = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), SAVE_PATH)
SAVE_FULL_PATH = SAVE_FULL_PATH.replace('\\', '/')
print(SAVE_FULL_PATH)
target = "file:///{}".format(SAVE_FULL_PATH)

# search
while True:
    terms = input("Search for: ")
    while True:
        mode = input("Search by publishers? [y/n]:")
        if mode == 'y':
            info = db.search_by_conference(terms, PUBLISHERS, NUMBER_PER_PUBLISHER)
            break
        elif mode == 'n':
            info = db.search(terms, NUMBER_PER_SEARCH)
            break
        else:
            continue
    info = db.sort_by_year(info)
    hbuild.save_as_html(info, SAVE_PATH, heading=terms)
    webbrowser.open('file://' + SAVE_FULL_PATH)

