# -*- coding: utf-8 -*-

"""
https://home-assistant.io/components/sensor.command_line/
"""

#import urllib2
import json
#import numpy as np
import os
import argparse

try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2


class NanoPool:
    def __init__(self, wallet, coin):
        self.wallet = wallet
        self.base_url = os.path.join('https://api.nanopool.org/v1/', coin.lower())

    def get_balance(self):
        url = self.__get_miner_url('balance')
        return self.__get_data(url)

    def get_avg_hashrate(self):
        url = self.__get_miner_url('avghashrate')
        data = self.__get_data(url)
        return round(data['h6'], 1)

    def get_current_hashrate(self):
        url = self.__get_miner_url('hashrate')
        return round(self.__get_data(url), 1)
    
    def get_general_info(self):
        url = self.__get_miner_url('user')
        return self.__get_data(url)

    def get_history(self):
        url = self.__get_miner_url('history')
        return self.__get_data(url)

    def get_aprox_earnings(self):
        hashrate = self.get_avg_hashrate()
        url = '/'.join([self.base_url, 'approximated_earnings', str(hashrate)])
        return round(self.__get_data(url)['month']['coins'], 2)

    def get_coin_prices(self):
        url = '/'.join([self.base_url, 'prices'])
        return round(self.__get_data(url)['price_usd'], 2)

    def get_difficulty(self):
        offset = 0
        blocks = 1
        url = '/'.join([self.base_url, 'block_stats', str(offset), str(blocks)])
        return self.__get_data(url)[0]['difficulty'] / 10**6

    def get_time_until_payment(self, payment_limit=0.01):
        balance = self.get_balance()
        hourly_earning_rate = self.get_aprox_earnings() / 720
        hours_until_payment = (payment_limit - balance) / hourly_earning_rate
        if hours_until_payment < 0:
            return 0
        else:
            return round(hours_until_payment, 1)
    
    def get_total_payout(self):
        url = self.__get_miner_url('payments')
        payments = self.__get_data(url)
        total_payout = 0
        for payment in payments:
            total_payout += payment['amount']
        
        return round(total_payout, 4)

    def __get_data(self, url):
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

#        req = urllib2.Request(url, None, header)
#        response = urllib2.urlopen(req).read().decode("utf-8")
        req = Request(url=url, headers=header)
        response = urlopen(req).read().decode("utf-8")

        data = json.loads(response)
        if data['status'] is True:
            return data['data']
        else:
#            return np.nan
            return 0

    def __get_miner_url(self, data_req):
        return '/'.join([self.base_url, data_req, self.wallet])

    
if __name__ == '__main__':
#    print('runnning')
#    main()
    FUNCTION_MAP = ['balance',
                    'avg_hashrate',
                    'current_hashrate',
                    'general_info',
                    'history',
                    'aprox_earnings',
                    'coin_prices',
                    'difficulty',
                    'time_until_payment',
                    'total_payout']
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=FUNCTION_MAP)
    parser.add_argument('-w', '--wallet', type=str, help='wallet address', required=True)
    parser.add_argument('-c', '--currency', type=str, help='currency', required=True)
    
    args = parser.parse_args()

    wallet = args.wallet
    currency = args.currency
    
    nanopool = NanoPool(wallet, currency)
    print(getattr(nanopool, 'get_' + args.command)())
