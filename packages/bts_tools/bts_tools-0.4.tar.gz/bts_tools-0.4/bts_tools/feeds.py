#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bts_tools - Tools to easily manage the bitshares client
# Copyright (c) 2014 Nicolas Wack <wackou@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from . import core
from .core import hashabledict
from .feed_providers import YahooFeedProvider, BterFeedProvider, Btc38FeedProvider,\
    PoloniexFeedProvider, GoogleFeedProvider, BloombergFeedProvider, BitcoinAverageFeedProvider,\
    CCEDKFeedProvider, BitfinexFeedProvider, BitstampFeedProvider, YunbiFeedProvider,\
    CoinCapFeedProvider, CoinMarketCapFeedProvider, BittrexFeedProvider, ALL_FEED_PROVIDERS
from collections import deque, defaultdict
from contextlib import suppress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import threading
import itertools
import statistics
import logging

log = logging.getLogger(__name__)

"""BitAssets for which we check and publish feeds."""
YAHOO_ASSETS = {'GOLD', 'EUR', 'GBP', 'CAD', 'CHF', 'HKD', 'MXN', 'RUB', 'SEK', 'SGD',
                'AUD', 'SILVER', 'TRY', 'KRW', 'JPY', 'NZD'}

OTHER_ASSETS = {'TUSD', 'CASH.USD', 'TCNY', 'CASH.BTC', 'ALTCAP', 'STEEM'}

# BIT_ASSETS_INDICES = {'SHENZHEN': 'CNY',
#                       'SHANGHAI': 'CNY',
#                       'NASDAQC': 'USD',
#                       'NIKKEI': 'JPY',
#                       'HANGSENG': 'HKD'}
# deactivate those indices for now
BIT_ASSETS_INDICES = {}

BIT_ASSETS = {'BTC', 'USD', 'CNY'} | YAHOO_ASSETS | OTHER_ASSETS | BIT_ASSETS_INDICES.keys()

"""List of feeds that should be shown on the UI and in the logs. Note that we
always check and publish all feeds, regardless of this variable."""
DEFAULT_VISIBLE_FEEDS = ['USD', 'BTC', 'CNY', 'GOLD', 'EUR']

feeds = {}
nfeed_checked = 0
cfg = None
history_len = None
price_history = None
visible_feeds = DEFAULT_VISIBLE_FEEDS


def load_feeds():
    global cfg, history_len, price_history, visible_feeds
    cfg = core.config['monitoring']['feeds']
    history_len = int(cfg['median_time_span'] / cfg['check_time_interval'])
    price_history = {cur: deque(maxlen=history_len) for cur in BIT_ASSETS}
    visible_feeds = cfg.get('visible_feeds', DEFAULT_VISIBLE_FEEDS)


def weighted_mean(l):
    """return the weighted mean of a list of FeedPrices"""
    if len(l) == 1:
        return l[0].price
    total_volume = sum(f.volume for f in l)
    result = sum(f.price*f.volume for f in l) / total_volume
    log.debug('Weighted mean for {}/{}: {:.4g}'.format(l[0].cur, l[0].base, result))
    log.debug('Exchange      Price          Volume          Contribution')
    for f in l:
        percent = 100 * f.volume / total_volume
        log.debug('{:14s} {:12.4g} {:14.2f} {:14.2f}%'.format(f.provider, f.price, f.volume, percent))
    return result


def get_multi_feeds(func, args, providers, stddev_tolerance=None):
    result = []
    provider_list = []

    def get_price(pargs):
        args, provider = pargs
        return provider, args, getattr(provider, func)(*args)

    with ThreadPoolExecutor(max_workers=4) as e:
        for f in [e.submit(get_price, pargs)
                  for pargs in itertools.product(args, providers)]:
            with suppress(Exception):
                provider, args, price = f.result()
                result.append(price)
                provider_list.append(provider)

    if stddev_tolerance:
        feeds_per_market = [(k, list(v)) for k, v in itertools.groupby(result, lambda x: (x.cur, x.base))]
        for market, feed_list in feeds_per_market:
            if len(feed_list) < 2:
                continue  # cannot compute stddev with less than 2 elements
            price_list = [f.price for f in feed_list]
            price = statistics.mean(price_list)
            stddev = statistics.stdev(price_list, price) / price  # relative stddev
            if stddev > stddev_tolerance:
                log.warning('Feeds for {asset} are not consistent amongst providers: {feeds} (stddev = {stddev:.7f})'.format(
                    asset=market, stddev=stddev, feeds=str(feed_list)
                ))

    return result


def filter_market(feed_list, market):
    """market should be a tuple (cur, base)"""
    return [f for f in feed_list if (f.cur, f.base) == market]


def get_feed_prices():
    provider_names = {p.lower() for p in cfg['feed_providers']}
    active_providers = set()
    for name, provider in ALL_FEED_PROVIDERS.items():
        if name in provider_names:
            active_providers.add(provider())

    # get currency rates from yahoo
    # do not include:
    # - BTC as we don't get it from yahoo
    # - USD as it is our base currency
    yahoo = YahooFeedProvider()
    yahoo_prices = yahoo.get(YAHOO_ASSETS, 'USD')

    # 1- get the BitShares price in major markets: BTC, USD and CNY
    bter, btc38, poloniex, ccedk, bitcoinavg, bitfinex, bitstamp, yunbi = (
        BterFeedProvider(), Btc38FeedProvider(), PoloniexFeedProvider(),
        CCEDKFeedProvider(), BitcoinAverageFeedProvider(), BitfinexFeedProvider(),
        BitstampFeedProvider(), YunbiFeedProvider())

    # 1.1- first get the bts/btc valuation
    providers_bts_btc = {poloniex, ccedk, yunbi} & active_providers
    if not providers_bts_btc:
        log.warning('No feed providers for BTS/BTC feed price')
    all_feeds = get_multi_feeds('get', [('BTS', 'BTC')], providers_bts_btc)

    # providers_bts_cny = {bter, btc38} & active_providers
    # if not providers_bts_cny:
    #     log.warning('No feed providers for BTS/CNY feed price')
    # all_feeds.update(get_multi_feeds('get', [('BTC', 'CNY'), ('BTS', 'CNY)')], providers_bts_cny))
    #
    # feeds_btc_cny = all_feeds[('BTC', 'CNY')]
    # if not feeds_btc_cny:
    #     raise core.NoFeedData('Could not get any BTC/CNY feeds')
    # btc_cny = weighted_mean(feeds_btc_cny)
    # cny_btc = 1 / btc_cny

    feeds_bts_btc = filter_market(all_feeds, ('BTS', 'BTC')) #+ [(p[0]*cny_btc, p[1]) for p in all_feeds[('BTS', 'CNY')]]
    if not feeds_bts_btc:
        raise core.NoFeedData('Could not get any BTS/BTC feeds')

    btc_price = weighted_mean(feeds_bts_btc)

    # 1.2- get the btc/usd (bitcoin avg)
    try:
        feeds_btc_usd = [bitcoinavg.get('BTC', 'USD')]
    except Exception:
        # fall back on Bitfinex, Bitstamp if BitcoinAverage is down - TODO: add Kraken, others?
        log.debug('Could not get USD/BTC')
        feeds_btc_usd = get_multi_feeds('get', [('BTC', 'USD')], {bitfinex, bitstamp})

    btc_usd = weighted_mean(feeds_btc_usd)

    usd_price = btc_price * btc_usd

    # 1.3- get the bts/cny valuation directly from cny markets. Going from bts/btc and
    #      btc/cny to bts/cny introduces a slight difference (2-3%) that doesn't exist on
    #      the actual chinese markets
    providers_bts_cny = {bter, btc38, yunbi} & active_providers

    # TODO: should go at the beginning: submit all fetching tasks to an event loop / threaded executor,
    # compute valuations once we have everything
    #all_feeds.append(get_multi_feeds('get', [('BTS', 'CNY')], providers_bts_cny))
    feeds_bts_cny = get_multi_feeds('get', [('BTS', 'CNY')], providers_bts_cny)
    if not feeds_bts_cny:
        # if we couldn't get the feeds for cny, try picking up our last value
        if price_history.get('cny'):
            log.warning('Could not get any BTS/CNY feeds, using last feed price')
            bts_cny = price_history['cny'][-1]
        else:
            raise core.NoFeedData('Could not get any BTS/CNY feeds')
    else:
        bts_cny = weighted_mean(feeds_bts_cny)

    cny_price = bts_cny

    feeds['BTC'] = btc_price
    feeds['CASH.BTC'] = btc_price
    feeds['USD'] = usd_price
    feeds['TUSD'] = usd_price
    feeds['CASH.USD'] = usd_price
    feeds['CNY'] = cny_price
    feeds['TCNY'] = cny_price

    log.debug('Got btc/usd price: {}'.format(btc_usd))
    log.debug('Got usd price: {}'.format(usd_price))
    log.debug('Got cny price: {}'.format(cny_price))

    # 2- now get the BitShares price in all other required currencies
    for cur, yprice in yahoo_prices.items():
        feeds[cur] = usd_price / yprice

    # 3- get the feeds for major composite indices
    providers_quotes = {yahoo, GoogleFeedProvider(), BloombergFeedProvider()}

    all_quotes = get_multi_feeds('query_quote',
                                 BIT_ASSETS_INDICES.items(), providers_quotes & active_providers,
                                 stddev_tolerance=0.02)

    for asset, cur in BIT_ASSETS_INDICES.items():
        feeds[asset] = 1 / statistics.mean(f.price for f in filter_market(all_quotes, (asset, cur)))

    # 4- get other assets
    altcap = get_multi_feeds('get', [('ALTCAP', 'BTC')], {CoinCapFeedProvider(), CoinMarketCapFeedProvider()},
                             stddev_tolerance=0.03)
    altcap = statistics.mean(f.price for f in altcap)
    feeds['ALTCAP'] = altcap

    steem_usd = BittrexFeedProvider().get('STEEM', 'BTC').price * btc_usd
    feeds['STEEM'] = steem_usd

    # 5- update price history for all feeds
    for cur, price in feeds.items():
        price_history[cur].append(price)


def median_str(cur):
    try:
        return statistics.median(price_history[cur])
    except Exception:
        return 'N/A'

def format_qualifier(c):
    if c in {'BTC', 'GOLD', 'SILVER'} | set(BIT_ASSETS_INDICES.keys()):
        return '%g'
    return '%f'


def get_fraction(price, asset_precision, base_precision, N=8):
    """Find nice fraction with at least N significant digits in
    both the numerator and denominator."""
    numerator = int(price * 10 ** asset_precision)
    denominator = 10 ** base_precision
    multiplier = 0
    while len(str(numerator)) < N and len(str(denominator)) < N:
        multiplier += 1
        numerator = int(price * 10 ** (asset_precision + multiplier))
        denominator = 10 ** (base_precision + multiplier)
    return numerator, denominator


def check_feeds(nodes):
    # TODO: update according to: https://bitsharestalk.org/index.php?topic=9348.0;all
    global nfeed_checked

    try:
        feed_period = int(cfg['publish_time_interval'] / cfg['check_time_interval'])
    except KeyError:
        feed_period = None
    feed_slot = cfg.get('publish_time_slot', None)

    # FIXME: seems like updating or checking last_updated doesn't work...
    last_updated = datetime.utcnow() - timedelta(days=1)

    def should_publish():
        if feed_period is not None and nfeed_checked % feed_period == 0:
            log.debug('Should publish because time interval has passed: {} seconds'.format(cfg['publish_time_interval']))
            return True
        now = datetime.utcnow()
        check_time_interval_minutes = cfg['check_time_interval'] // 60 + 1
        if feed_slot is not None:
            start_slot = feed_slot
            end_slot = feed_slot + check_time_interval_minutes
            if (((start_slot <= now.minute <= end_slot) or
                 (end_slot >= 60 and now.minute <= end_slot % 60)) and
                now - last_updated > timedelta(minutes=max(3*check_time_interval_minutes, 50))):

                log.debug('Should publish because time slot has arrived: time {:02d}:{:02d}'.format(now.hour, now.minute))
                return True
        log.debug('No need to publish feeds')
        return False

    try:
        get_feed_prices()
        nfeed_checked += 1

        def fmt(feeds):
            fmt = ', '.join('%s %s' % (format_qualifier(c), c) for c in visible_feeds)
            msg = fmt % tuple(feeds[c] for c in visible_feeds)
            return msg

        publish_status = ''
        if feed_period:
            publish_status += ' [%d/%d]' % (nfeed_checked, feed_period)
        if feed_slot:
            publish_status += ' [min={:02d}]'.format(feed_slot)

        log.debug('Got feeds: %s %s' % (fmt(feeds), publish_status))

        for node in nodes:
            if node.type != 'feed_publisher':
                continue

            # TODO: dealt with as an exceptional case for now, should be refactored
            if node.bts_type() == 'steem':
                price = statistics.median(price_history['STEEM'])
                # check whether we need to publish again:
                # - if published more than 12 hours ago, publish again
                # - if published price different by more than 3%, publish again
                if 'last_price' in node.opts:  # make sure we have already published once
                    if not (datetime.utcnow() - node.opts['last_published'] > timedelta(hours=12) or
                            (price - node.opts['last_price']) / node.opts['last_price'] >= 0.03):
                        continue
                # publish median value of the price, not latest one
                price_obj = {'base': '{:.3} SBD'.format(price), 'quote': '1.000 STEEM'}
                log.info('Node %s publishing feed price for steem: %s SBD' % (node.name, price))
                node.publish_feed(node.name, price_obj, True)
                node.opts['last_price'] = price
                node.opts['last_published'] = datetime.utcnow()
                continue


            # if an exception occurs during publishing feeds for a delegate (eg: standby delegate),
            # then we should still go on for the other nodes (and not let exceptions propagate)
            try:
                if should_publish():
                    if not node.is_online():
                        log.warning('Cannot publish feeds for delegate %s: client is not running' % node.name)
                        continue
                    if node.is_locked():
                        log.warning('Cannot publish feeds for delegate %s: wallet is locked' % node.name)
                        continue
                    # publish median value of the price, not latest one
                    median_feeds = {c: statistics.median(price_history[c]) for c in feeds}
                    log.info('Node %s publishing feeds: %s' % (node.name, fmt(median_feeds)))
                    if node.is_graphene_based():
                        DISABLED_ASSETS = ['RUB', 'SEK',  # black swan
                                           'STEEM']       # not on bitshares


                        def get_price_for_publishing(asset, price):
                            c = cfg['asset_params'].get(asset) or cfg['asset_params']['default']
                            asset_id = node.asset_data(asset)['id']
                            asset_precision = node.asset_data(asset)['precision']

                            base = 'BTS'
                            if asset == 'ALTCAP':
                                base = 'BTC'
                            base_id = node.asset_data(base)['id']
                            base_precision = node.asset_data(base_id)['precision']
                            bts_precision = node.asset_data('BTS')['precision']

                            numerator, denominator = get_fraction(price, asset_precision, base_precision)

                            # CER price needs to be priced in BTS always. Get conversion rate
                            # from the base currency to BTS, and use it to scale the CER price

                            if base != 'BTS':
                                base_bts_price = median_feeds[base]
                                cer_price = price * base_bts_price / c['core_exchange_factor']
                                cer_numerator, cer_denominator = get_fraction(cer_price, base_precision, bts_precision)
                            else:
                                cer_numerator, cer_denominator = numerator, int(denominator*c['core_exchange_factor'])

                            price = {
                                'settlement_price': {
                                    'quote': {
                                        'asset_id': base_id,
                                        'amount': denominator
                                    },
                                    'base': {
                                        'asset_id': asset_id,
                                        'amount': numerator
                                    }
                                },
                                'maintenance_collateral_ratio': c['maintenance_collateral_ratio'],
                                'maximum_short_squeeze_ratio': c['maximum_short_squeeze_ratio'],
                                'core_exchange_rate': {
                                    'quote': {
                                        'asset_id': '1.3.0',
                                        'amount': cer_denominator
                                    },
                                    'base': {
                                        'asset_id': asset_id,
                                        'amount': cer_numerator
                                    }
                                }
                            }
                            return price

                        # first, try to publish all of them in a single transaction
                        try:
                            handle = node.begin_builder_transaction()
                            for asset, price in median_feeds.items():
                                if asset in DISABLED_ASSETS:
                                    # markets temporarily disabled because they are in a black swan state
                                    continue
                                op = [19,  # id 19 corresponds to price feed update operation
                                      hashabledict({"asset_id": node.asset_data(asset)['id'],
                                                    "feed": get_price_for_publishing(asset, price),
                                                    "publisher": node.get_account(node.name)["id"]})
                                      ]
                                node.add_operation_to_builder_transaction(handle, op)

                            # set fee
                            node.set_fees_on_builder_transaction(handle, '1.3.0')

                            # sign and broadcast
                            node.sign_builder_transaction(handle, True)

                        except Exception as e:
                            log.error('tried single transaction for all feeds, failed because:')
                            log.exception(e)

                            # if an error happened, publish feeds individually to make sure that
                            # at least the ones that work can get published
                            for asset, price in median_feeds.items():
                                if asset in DISABLED_ASSETS:
                                    # markets temporarily disabled because they are in a black swan state
                                    continue
                                # publish all feeds even if a single one fails
                                try:
                                    price = hashabledict(get_price_for_publishing(asset, price))
                                    node.publish_asset_feed(node.name, asset, price, True)  # True: sign+broadcast
                                except Exception as e:
                                    log.exception(e)

                    else:
                        feeds_as_string = [(cur, '{:.10f}'.format(price)) for cur, price in median_feeds.items()]
                        node.wallet_publish_feeds(node.name, feeds_as_string)

                    last_updated = datetime.utcnow()

            except Exception as e:
                log.exception(e)

    except core.NoFeedData as e:
        log.warning(e)

    except Exception as e:
        log.exception(e)

    threading.Timer(cfg['check_time_interval'], check_feeds, args=(nodes,)).start()
