Small crawler for crypto exchange markets
=========================================

Created: romiq.kh@gmail.com, 2021

1. Download current rates for:
    * Exmo
    * Kraken
    * Poloniex
2. Display sorted currencies pair (supported USD-BTC, USD-ETH, BTC-XRP, BTC-ETH, USD-LTC),

````
---------- BTC -> USD ----------
  ASK: Poloniex - 58058.221 | Kraken - 58088
  BID: Poloniex - 58047.307 | Kraken - 58067.5
---------- ETH -> USD ----------
  ASK: Poloniex - 2069.8753 | Kraken - 2071.9000
  BID: Poloniex - 2069.3161 | Kraken - 2070.8000
---------- XRP -> BTC ----------
  ASK: Poloniex - 0.00001689
  BID: Poloniex - 0.00001687
---------- ETH -> BTC ----------
  ASK: Poloniex - 0.03564706
  BID: Poloniex - 0.03564431
---------- LTC -> USD ----------
  ASK: Poloniex - 224.96055 | Kraken - 225.19000
  BID: Poloniex - 224.82855 | Kraken - 224.89000

````

To disable certain crawler (for e.g. due certain network errors) use followinf flags:
* DISABLE_KRAKENCRAWLER=1 - to disabled Kraken
* DISABLE_EXMOCRALER=1 - to disabled Exmo
* DISABLE_POLONIEXCRAWLER=1 - to disabled Poloniex


Running in docker container
---------------------------
By default docker will be crawl every 2 minits.

1. Build container

`docker build . -t crawler`

2. Run

`docker run -it --rm crawler`
