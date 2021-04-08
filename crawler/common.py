# -*- coding: utf-8 -*-
# romiq.kh@gmail.com, 2021
import json
import os
from collections import OrderedDict
import decimal

import aiohttp


class BaseCrawler:

    def __init__(self, cfg):
        self.raw_cfg = cfg

    async def fetch_ask_bid(self, pairs):
        raise NotImplementedError()


class KrakenCrawler(BaseCrawler):
    KRAKEN_BASE_URL = "https://futures.kraken.com/derivatives/api/v3/tickers"

    def __init__(self, cfg):
        super().__init__(cfg)

        cfg = cfg or {}
        self.base_url = cfg.get("url") or self.KRAKEN_BASE_URL

    async def fetch_ask_bid(self, pairs):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                values = await response.json()
                if self.raw_cfg.get("save_data"):
                    with open(os.path.join(".", "samples", "kraken.json"), "w",
                            encoding = "utf-8") as df:
                        json.dump(values, df)
                return self.decode_courses(values, pairs)

    def decode_courses(self, data, pairs):
        ENC_CODE = {
            "BTC": "XBT",
        }

        if data.get("result") != "success":
            raise Exception("Failed to fetch data")

        result = {}

        req_pairs = OrderedDict()
        for c1, c2 in pairs:
            ec1 = ENC_CODE.get(c1) or c1
            ec2 = ENC_CODE.get(c2) or c2
            req_pairs["{}:{}".format(ec2, ec1)] = (c1, c2, False)
            req_pairs["{}:{}".format(ec1, ec2)] = (c1, c2, True)

        for tick in data.get("tickers"):
            pair = tick.get("pair")
            if pair in req_pairs and tick.get("tag") == "perpetual":
                c1, c2, reverse = req_pairs[pair]
                if (c2, c1) in result: continue
                result[(c1, c2)] = {
                    "ask": decimal.Decimal(tick.get("ask")),
                    "bid": decimal.Decimal(tick.get("bid")),
                    "reverse": reverse,
                }

        return self.__class__.__name__, result


class VariantOneCrawler(BaseCrawler):
    BASE_URL = None
    ENC_CODE = None
    TEST_FILE = None
    ASK_KEY = None
    BID_KEY = None
    REVERSED = False

    def __init__(self, cfg):
        super().__init__(cfg)

        cfg = cfg or {}
        self.base_url = cfg.get("url") or self.BASE_URL

    async def fetch_ask_bid(self, pairs):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                values = await response.json()
                if self.raw_cfg.get("save_data"):
                    with open(os.path.join(".", "samples", self.TEST_FILE), "w",
                            encoding = "utf-8") as df:
                        json.dump(values, df)
                return self.decode_courses(values, pairs)

    def decode_courses(self, data, pairs):

        def search_pair(data, pair_name):
            if pair_name not in data: return None
            raw = data[pair_name]
            value = {
                "ask": decimal.Decimal(raw.get(self.ASK_KEY)),
                "bid": decimal.Decimal(raw.get(self.BID_KEY))
            }
            return value

        result = {}

        for c1, c2 in pairs:
            ec1 = self.ENC_CODE.get(c1) or c1
            ec2 = self.ENC_CODE.get(c2) or c2
            raw = search_pair(data, "{}_{}".format(ec1, ec2))
            if raw:
                raw["reverse"] = self.REVERSED
                result[(c1, c2)] = raw
                continue
            raw = search_pair(data, "{}_{}".format(ec2, ec1))
            if raw:
                raw["reverse"] = not self.REVERSED
                result[(c1, c2)] = raw

        return self.__class__.__name__, result


class PoloniexCrawler(VariantOneCrawler):
    BASE_URL = "https://poloniex.com/public?command=returnTicker"
    ENC_CODE = {
        "USD": "USDT",
    }
    TEST_FILE = "poloniex.json"
    ASK_KEY = "lowestAsk"
    BID_KEY = "highestBid"
    REVERSED = False


class ExmoCrawler(VariantOneCrawler):
    BASE_URL = "https://api.exmo.com/v1.1/ticker"
    ENC_CODE = {
    }
    TEST_FILE = "exmo.json"
    ASK_KEY = "sell_price"
    BID_KEY = "buy_price"
    REVERSED = True
