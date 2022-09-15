import xml.etree.ElementTree as et
import requests as re
from utils.logging import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

urllib3.disable_warnings()

ATTRIBUTES = ['authors', 'title', 'venue', 'publisher', 'year', 'type', 'key', 'url', 'doi', 'ee']


def fetch(url):
    log(STD_INFO + 'Fetching ' + url)
    return re.get(url, verify=False).text


def get_xml(terms, number, batch_size=100):
    """
    :param terms: string of searched terms
    :param number: number of results
    :param batch_size: number of results extracted from dblp each time
    :return: a list of xml strings
    """
    xml = []
    if number < batch_size:
        url = 'https://dblp.org/search/publ/api?q=' + str(terms) + '&h=' + str(number)
        xml += [fetch(url)]
    else:
        batch_number = int(number / batch_size)
        for batch in range(0, batch_number):
            url = 'https://dblp.org/search/publ/api?q=' + str(terms) + '&h=' + str(batch_size) + '&f=' + str(
                batch * batch_size)
            xml += [fetch(url)]
        if number % batch_size is not 0:
            url = 'https://dblp.org/search/publ/api?q=' + str(terms) + '&h=' + str(number % batch_size) + '&f=' + str(
                batch_number * batch_size)
            xml += [fetch(url)]
    return xml

# def get_xml(terms, number):
#     """
#     :param terms: string of searched terms
#     :param number: number of results
#     :param batch_size: number of results extracted from dblp each time
#     :return: a list of xml strings
#     """
#     xml = []
#     url = 'https://dblp.org/search/publ/api?q=' + str(terms) + '&h=' + str(number)
#     xml += [fetch(url)]
#     return xml


def get_attribute(info):
    """
    transform <info> elements to a list of dictionaries
    :param info: a list of <info> elements
    :return: a list of dictionaries containing attributes
    """
    global ATTRIBUTES
    attributes = []
    for inf in info:
        dic = {}
        for attribute in ATTRIBUTES:
            if attribute == 'authors':
                aut = ''
                try:
                    for author in inf.find('./authors').findall('./*'):
                        aut += author.text + ', '
                except AttributeError:
                    aut = 'null'
                dic[attribute] = aut
            else:
                try:
                    elem = inf.find('./' + attribute).text
                except AttributeError:
                    elem = 'null'
                dic[attribute] = elem
        attributes += [dic]
    return attributes


def get_info(xml):
    """
    :param xml: the list of xml strings
    :return: a list of dictionaries containing attributes of all entries
    """
    elements = []
    for x in xml:
        tree = et.fromstring(x, parser=et.XMLParser(encoding='utf-8'))
        info = tree.findall('.//info')
        elements += info
    elements = get_attribute(elements)
    return elements


def search(terms, number, batch_size=100):
    """
    direct search by terms
    :param terms: search terms
    :param number: number of results
    :param batch_size: number of results loaded by get_xml() each time
    :return: a list of <info> elements
    """
    xml = get_xml(terms, number, batch_size=batch_size)
    info = get_info(xml)
    return info


def sort_by_year(info, descending=True):
    def year(e):
        return int(e['year'])
    if descending:
        info.sort(key=year, reverse=True)
    else:
        info.sort(key=year, reverse=False)
    return info


def search_by_conference(terms, conferences, number_per_conference=50, max_workers=10):
    """
    search by conferences
    :param max_workers: max workers of thread pool executor
    :param terms: search terms
    :param conferences: a list of conferences
    :param number_per_conference: number of results for each conference
    :return: a list of <info> elements
    """
    xml = []
    terms_ = []
    for conf in conferences:
        terms_ += [conf+' '+terms]

    threads = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in terms_:
            threads.append(executor.submit(get_xml, _, number_per_conference, batch_size=100))

        for task in as_completed(threads):
            xml += task.result()

    info = get_info(xml)
    return info


if __name__ == '__main__':
    xml = get_xml('mobicom', 20)
    info = get_info(xml)
    _, text = get_attribute(info, 'ee')

