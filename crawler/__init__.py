# -*- coding: utf-8 -*-
# romiq.kh@gmail.com, 2021

import asyncio
import json
import os
import pprint
import decimal

from .common import BaseCrawler, PoloniexCrawler, KrakenCrawler, ExmoCrawler

pairs = [
    ["USD", "BTC"],
    ["USD", "ETH"],
    ["BTC", "XRP"],
    ["BTC", "ETH"],
    ["USD", "LTC"],
]

crawlers = [KrakenCrawler, PoloniexCrawler, ExmoCrawler]


async def amain():

    crawler_instances = []
    for crawler_cls in crawlers:
        if not os.environ.get("DISABLE_" + crawler_cls.__name__.upper()):
            crawler_instances.append(crawler_cls({}))

    result = await asyncio.gather(*[
        x.fetch_ask_bid(pairs = pairs) for x in crawler_instances],
    )
    do_group(result)


def test_kraken():
    kraken = KrakenCrawler({})
    with open("samples/kraken.json", "r", encoding = "utf-8") as sf:
        values = json.load(sf)
    pprint.pprint(kraken.decode_courses(values, pairs = pairs))


def test_poloneix():
    poloniex = PoloniexCrawler({})
    with open("samples/poloniex.json", "r", encoding = "utf-8") as sf:
        values = json.load(sf)
    pprint.pprint(poloniex.decode_courses(values, pairs = pairs))


def test_exmo():
    exmo = ExmoCrawler({})
    with open("samples/exmo.json", "r", encoding = "utf-8") as sf:
        values = json.load(sf)
    pprint.pprint(exmo.decode_courses(values, pairs = pairs))


def load_fetched_data():
    data = []

    for crawler_cls in crawlers:
        crawler = crawler_cls({})
        name = crawler_cls.__name__
        if name.endswith("Crawler"):
            name = name[:-7]
        with open(os.path.join(".", "samples", "{}.json".format(name.lower())),
                "r", encoding = "utf-8") as sf:
            values = json.load(sf)
            data.append(crawler.decode_courses(values, pairs = pairs))

    return data


def do_group(couses_list):
    print("=" * 32)
    for c1, c2 in pairs:
        print("-" * 10, "{} -> {}".format(c2, c1), "-" * 10)
        ask_list = []
        bid_list = []
        for crawler_name, courses in couses_list:
            name = crawler_name
            if name.endswith("Crawler"):
                name = name[:-7]
            if (c1, c2) in courses:
                rate = courses[(c1, c2)]
                ask_list.append([rate.get("ask"), name])
                bid_list.append([rate.get("bid"), name])

        for lst_name, lst in (("ASK", ask_list), ("BID", bid_list)):
            line = []
            for rate, name in sorted(lst):
                line.append("{} - {:.8g}".format(name, rate))
            print("  {}:".format(lst_name), " | ".join(line))


def main():
    # test_kraken()
    # test_poloneix()
    # test_exmo()
    #data = load_fetched_data()
    #do_group(data)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
