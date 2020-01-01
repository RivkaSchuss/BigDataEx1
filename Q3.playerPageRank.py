import collections
import random
from collections import Counter


def should_follow_link():
    return random.random() > 0.15


def create_url_dict_from_list(list_of_pairs):
    result_dict = collections.defaultdict(list)
    for url_tuple in list_of_pairs:
        if len(url_tuple) == 2:
            result_dict[url_tuple[0]].append(url_tuple[1])
        else:
            print("Invalid tuple: {0}, not adding to dict".format(url_tuple))
    return result_dict


def calc_pagerank(visit_count_dict, steps):
    page_rank = {}
    for url, visits in visit_count_dict.items():
        page_rank[url] = visits / steps
    return page_rank


def visit_random_url(url_dict, visit_dict):
    url = random.choice(list(url_dict))
    visit_dict[url] += 1
    return url_dict[url]


def visit_pages(visits, steps, url_dict):
    list_of_outgoing_links = visit_random_url(url_dict, visits)

    for step in range(1, steps): # first step out of the loop
        if len(list_of_outgoing_links) != 0:
            if should_follow_link():
                target = random.choice(list_of_outgoing_links)
                visits[target] += 1
                if target in url_dict:
                    list_of_outgoing_links = url_dict[target]
                else:
                    # sink
                    list_of_outgoing_links = []
            else:
                # random link with prob 0.15
                list_of_outgoing_links = visit_random_url(url_dict, visits)
        else:
            # no outgoing links - random link
            list_of_outgoing_links = visit_random_url(url_dict, visits)


def playerPageRank(listOfPairs):
    if len(listOfPairs) == 0:
        print("Got empty list, nothing to do...")
        return {}
    url_dict = create_url_dict_from_list(listOfPairs)
    if len(url_dict) == 0:
        print("Generated empty url_dict, nothing to do...")
        return {}

    steps = 100000
    first_iter_visit_dict = Counter()
    visit_pages(first_iter_visit_dict, steps, url_dict)
    page_rank_first_iter = calc_pagerank(first_iter_visit_dict, steps=steps)

    second_iter_visit_dict = Counter()
    visit_pages(second_iter_visit_dict, steps, url_dict)
    page_rank_second_iter = calc_pagerank(second_iter_visit_dict, steps=steps)

    merged_page_rank = collections.defaultdict(list)
    for d in (page_rank_first_iter, page_rank_second_iter):
        for key, value in d.items():
            merged_page_rank[key].append(value)

    return dict(merged_page_rank)
