from time import sleep

import lxml.html
import requests
from pqdict import pqdict
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s', level=logging.DEBUG)
LOGGER = logging.getLogger()


def insert_url_to_priority_queue(url, priority_queue_urls):
    if url in priority_queue_urls:
        current_priority = priority_queue_urls.pop(url)
        priority_queue_urls[url] = current_priority + 1
        LOGGER.info("added url: {0} with priority {1}".format(url, current_priority + 1))
    else:
        priority_queue_urls[url] = 1
        LOGGER.info("added url: {0} with priority {1}".format(url, 1))


def crawl_with_priority(crawled_urls, priority_queue_urls, xpaths, list_of_url_tuples):
    wiki_prefix = 'https://en.wikipedia.org'
    while len(crawled_urls) < 100:
        url_to_crawl = priority_queue_urls.pop()
        LOGGER.info("crawling {0}".format(url_to_crawl))
        crawled_urls.add(url_to_crawl)
        res = requests.get(url_to_crawl)
        doc = lxml.html.fromstring(res.content)
        for xpath in xpaths:
            for t in doc.xpath(xpath):
                if not str(t).startswith(wiki_prefix):
                    current_url = wiki_prefix + str(t)
                else:
                    current_url = str(t)
                list_of_url_tuples.append([url_to_crawl, current_url])
                if current_url not in crawled_urls:
                    insert_url_to_priority_queue(current_url, priority_queue_urls)
                LOGGER.info("extracted {0} from url: {1}".format(current_url, url_to_crawl))
        sleep(1)
    no_duplicates = set(map(tuple, list_of_url_tuples))
    return list(map(list, no_duplicates))


def crawl(url, xpaths):
    list_of_url_tuples = []
    priority_queue_urls = pqdict({url: 1}, reverse=True)  # max-heap priority-queue
    crawled_urls = set()
    return crawl_with_priority(crawled_urls, priority_queue_urls, xpaths, list_of_url_tuples)


a = crawl('https://en.wikipedia.org/wiki/Andy_Ram',
          ["//text()[contains(., 'against')]/following-sibling::a/@href[contains(., 'wiki')]"])
LOGGER.info("number of tuples: {0}".format(len(a)))
