import dominate
from dominate.tags import *
from utils.logging import *
from utils.path import *
from config import settings


def save_as_html(info, path, heading=None):
    """
    save a list of <info> elements as html file
    :param info: a list of dictionaries containing attributes of all entries
    :param path: path to output html file
    :param heading: a string as the title of the html page
    :return:
    """
    doc = dominate.document(title='dblp searching results')
    with doc:
        if heading is not None:
            h1(str(heading))
        h3(str(len(info)) + ' results')

        for _ in range(len(info)):
            info_entry(settings['entry_style'], info[_])
            # li(a(info[_]['year'] + ', ' + info[_]['venue'] + ': ' + info[_]['title'], href=info[_]['ee']))

    mkdir(path_parent(path))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(doc))
    log(STD_INFO + 'Successfully saved to ' + path)


def info_entry(style_, info):
    if style_['style'] == 'default':
        li(a(info['year'] + ', ' + info['venue'] + ': ' + info['title'], href=info['ee'])
           , style="line-height:{}px".format(style_['line_height']))
    elif style_['style'] == 'rainbow':
        li(
            span(info['year'], style="color:{};".format(style_['rainbow_color']['year'])),
            " ",
            span(info['venue'], style="color:{};".format(style_['rainbow_color']['venue'])),
            " ",
            span(info['title'], style="color:{};".format(style_['rainbow_color']['title'])),
            " ",
            a("paper", href=info['ee'])
            , style="line-height:{}px".format(style_['line_height']))
    else:
        raise ValueError("unknown entry type")
