import collections
import random
from collections import Counter
from time import sleep

import lxml.html
import requests
from pqdict import pqdict
import logging


def should_follow_link():
    return random.random() > 0.15


def create_url_dict_from_list(list_of_pairs):
    result_dict = collections.defaultdict(list)
    for url_tuple in list_of_pairs:
        result_dict[url_tuple[0]].append(url_tuple[1])
    return result_dict


def calc_pagerank(visit_count_dict, steps):
    page_rank = {}
    for url, visits in visit_count_dict.items():
        page_rank[url] = visits / steps
    return page_rank


def get_random_value_from_dict(url_dict):
    key = random.choice(list(url_dict))
    return url_dict[key]


def playerPageRank(listOfPairs):
    steps = 100000
    url_dict = create_url_dict_from_list(listOfPairs)
    list_of_outgoing_links = get_random_value_from_dict(url_dict)
    visits = Counter()
    for step in range(0, steps):
        if len(list_of_outgoing_links) != 0:
            if should_follow_link():
                target = random.choice(list_of_outgoing_links)
                visits[target] += 1
                if target in url_dict:
                    list_of_outgoing_links = url_dict[target]
                else:
                    list_of_outgoing_links = []  # sink
            else:
                # random link with prob 0.15
                list_of_outgoing_links = get_random_value_from_dict(url_dict)
        else:
            # no outgoing links - random link
            list_of_outgoing_links = get_random_value_from_dict(url_dict)
    page_rank = calc_pagerank(visits, steps=steps)
    print(page_rank)
