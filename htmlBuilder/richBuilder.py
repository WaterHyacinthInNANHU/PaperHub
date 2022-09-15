from os.path import dirname, realpath, join
import config
from utils.path import mkdir
from copy import copy
from bs4 import BeautifulSoup
from utils.logging import *


# logging path
_logging_path = join(config.root, "output")
mkdir(_logging_path)

# resource path
_dir_path_of_this_file = dirname(realpath(__file__))
_resource_path = join(_dir_path_of_this_file, 'resources')

# load templates
with open(join(_resource_path, 'entry_temp.html')) as _f:
    _entry_temp = BeautifulSoup(_f, features="html.parser").find('a')

# make soup with temp
with open(join(_resource_path, 'log_temp.html')) as f:
    html_soup = BeautifulSoup(f, features="html.parser")


def get_logging_file_path(filename: str) -> str:
    path = join(_logging_path, filename)
    return path


def _write_entry(title: list, paper_link: str, id_: int):
    # create entry from temp
    entry = copy(_entry_temp)
    # sign entry
    entry['data-target'] = '#{}'.format(id_)
    entry.div['id'] = '{}'.format(id_)
    entry.p.a['herf'] = paper_link
    # embed title
    cnt = 0
    for index, item in enumerate(entry.p.children):
        if item.name == "span":
            item.string = str(title[cnt])
            cnt += 1
    # embed sub-page
    entry.div.object['data'] = paper_link
    entry.div.object.embed['src'] = paper_link
    # entry.div.iframe['src'] = paper_link
    # add to soup
    html_soup.html.body.div.append(entry)


def save_as_html(info, topic):
    saving_path = get_logging_file_path("PaperHub_Searching_Result__{}.html".format(topic))
    # body
    for index, item in enumerate(info):
        _write_entry([item['year'], item['venue'], item['title']], item['ee'], index)
    # header
    html_soup.html.head.title.string = "PaperHub: {}".format(topic)
    html_soup.html.body.h1.string = topic
    html_soup.html.body.h3.string = '{} results'.format(str(len(info)))
    with open(saving_path, 'w', encoding='utf-8') as f_:
        f_.write(str(html_soup))
    log('{}{} results have been successfully saved to {}'.format(STD_INFO, str(len(info)), saving_path))
