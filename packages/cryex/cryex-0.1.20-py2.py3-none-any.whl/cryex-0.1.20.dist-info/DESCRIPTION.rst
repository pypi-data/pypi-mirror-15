Cryex
=====

Clients for various cryptocurrency exchanges.

|Build Status|

Exchanges supported:
~~~~~~~~~~~~~~~~~~~~

-  Kraken
-  Poloniex

Features supported:
~~~~~~~~~~~~~~~~~~~

-  Get ticker
-  ... more to come ...

Usage:
~~~~~~

.. code:: python

    from cryex import Poloniex, Kraken


    # Public
    client = Poloniex()
    ticker_data = client.public.ticker('eth_btc')
    trades = client.public.trades('eth_btc')
    currencies = client.public.currencies()

    # Private
    client = Poloniex(key='your-key', secret='your-secret')
    bal = client.private.balances()
    bath_eth = client.private.balances('eth')

    client.private.buy('eth_btc', price, amount)

    print(ticker_data)

::

    {
        'low24h': 0.0110211,
        'last': 0.0121899,
        'exchange': 'poloniex',
        'volume24h': 1350859.34589662,
        'high24h': 0.0140101,
        'pair': 'eth_btc'
    }

FAQ:
~~~~

-  Why are you using namedtuple objects for asks, bids and public
   trades? To save space.

.. |Build Status| image:: https://travis-ci.org/walkr/cryex.svg?branch=master
   :target: https://travis-ci.org/walkr/cryex


=======
History
=======

0.1.0 (2016-1-22)
------------------

* First release on PyPI.

0.1.2

* Return ticker values as `Decimal`

