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


def get_random_value_from_dict(url_dict):
    key = random.choice(list(url_dict))
    return url_dict[key]


def visit_pages(visits, list_of_outgoing_links, steps, url_dict):
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


def playerPageRank(listOfPairs):
    if len(listOfPairs) == 0:
        print("Got empty list, nothing to do...")
        return {}
    url_dict = create_url_dict_from_list(listOfPairs)
    if len(url_dict) == 0:
        print("Generated empty url_dict, nothing to do...")
        return {}

    steps = 100000
    visit_dict = Counter()
    list_of_outgoing_links = get_random_value_from_dict(url_dict)
    visit_pages(visit_dict, list_of_outgoing_links, steps, url_dict)
    page_rank_first_100000_steps = calc_pagerank(visit_dict, steps=steps)

    visit_pages(visit_dict, list_of_outgoing_links, steps, url_dict)
    page_rank_second_100000_steps = calc_pagerank(visit_dict, steps=steps * 2)

    merged_page_rank = collections.defaultdict(list)
    for d in (page_rank_first_100000_steps, page_rank_second_100000_steps):
        for key, value in d.items():
            merged_page_rank[key].append(value)

    return dict(merged_page_rank)
