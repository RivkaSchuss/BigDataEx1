import urllib.robotparser
from time import sleep

import lxml.html
import requests
from pqdict import pqdict
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s', level=logging.WARNING)
LOGGER = logging.getLogger()


def insert_url_to_priority_queue(url, priority_queue_urls):
    if url in priority_queue_urls:
        current_priority = priority_queue_urls.pop(url)
        priority_queue_urls[url] = current_priority + 1
        LOGGER.info("added url: {0} with priority {1}".format(url, current_priority + 1))
    else:
        priority_queue_urls[url] = 1
        LOGGER.info("added url: {0} with priority {1}".format(url, 1))


def get_response(url):
    attempts = 3
    res = None
    for i in range(0, attempts):
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            res = None
            continue
        break  # if it reaches here, no exception has occurred
    return res


def crawl_with_priority(crawled_urls, priority_queue_urls, xpaths, list_of_url_tuples):
    wiki_prefix = 'https://en.wikipedia.org'
    robots_file_parser = urllib.robotparser.RobotFileParser()
    robots_file_parser.set_url("https://en.wikipedia.org/robots.txt")
    robots_file_parser.read()
    while len(crawled_urls) < 100:
        try:
            url_to_crawl = priority_queue_urls.pop()
        except KeyError:
            # pqdict is empty, nothing to do anymore
            break

        if not robots_file_parser.can_fetch("*", url_to_crawl):
            LOGGER.warning("Can't crawl url: {0} due to crawling ethics defined in robots.txt".format(url_to_crawl))
            continue  # can't crawl this URL, skipping...

        LOGGER.info("crawling {0}".format(url_to_crawl))
        crawled_urls.add(url_to_crawl)

        res = get_response(url_to_crawl)
        if res is None:
            LOGGER.error("Failed to get a response from url: {0}, skipping...".format(url_to_crawl))
            continue  # Error has occurred, skip this URL

        doc = lxml.html.fromstring(res.content)
        for xpath in xpaths:
            for t in doc.xpath(xpath):
                if "en.wikipedia.org" not in str(t) and (str(t).startswith("https://") or str(t).startswith("http://")):
                    # don't wander off wikipedia
                    LOGGER.warning("url: {0} is not in Wikipedia, not adding it".format(str(t)))
                    continue

                if str(t).startswith("/wiki"):
                    current_url = wiki_prefix + str(t)
                else:
                    current_url = str(t)

                list_of_url_tuples.append([url_to_crawl, current_url])
                if current_url not in crawled_urls:
                    insert_url_to_priority_queue(current_url, priority_queue_urls)
                LOGGER.info("extracted {0} from url: {1}".format(current_url, url_to_crawl))
        sleep(3)
    no_duplicates = set(map(tuple, list_of_url_tuples))
    return list(map(list, no_duplicates))


def crawl(url, xpaths):
    list_of_url_tuples = []
    priority_queue_urls = pqdict({url: 1}, reverse=True)  # max-heap priority-queue
    crawled_urls = set()
    return crawl_with_priority(crawled_urls, priority_queue_urls, xpaths, list_of_url_tuples)
