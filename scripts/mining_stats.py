# -*- coding: utf-8 -*-

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
        return self.__get_data(url)

    def get_current_hashrate(self):
        url = self.__get_miner_url('hashrate')
        return self.__get_data(url)
    
    def get_general_info(self):
        url = self.__get_miner_url('user')
        return self.__get_data(url)

    def get_history(self):
        url = self.__get_miner_url('history')
        return self.__get_data(url)

    def get_aprox_earnings(self, hashrate):
        url = '/'.join([self.base_url, 'approximated_earnings', str(hashrate)])
        return self.__get_data(url)

    def get_coin_prices(self):
        url = '/'.join([self.base_url, 'prices'])
        return self.__get_data(url)

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
                    'coin_prices']
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=FUNCTION_MAP)
    parser.add_argument('-w', '--wallet', type=str, help='wallet address', required=True)
    parser.add_argument('-c', '--currency', type=str, help='currency', required=True)
    
    args = parser.parse_args()

    wallet = args.wallet
    currency = args.currency
    
    nanopool = NanoPool(wallet, currency)
    print(getattr(nanopool, 'get_' + args.command)())
