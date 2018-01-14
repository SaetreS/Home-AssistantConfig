# -*- coding: utf-8 -*-

import json
import argparse
from datetime import datetime, timedelta
   
try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2

class AeonMiningPool:
    def __init__(self, wallet):
        self.wallet = wallet
        self.base_url = 'https://api.aeonminingpool.com/api'

    def get_balance(self):
        url = self.__get_miner_url()
        val = self.__get_data(url)['amtDue']
        return round(float(str(val)[:-12]+'.'+str(val)[-12:]), 4)

    def get_total_payout(self):
        url = self.__get_miner_url()
        val = self.__get_data(url)['amtPaid']
        return round(float(str(val)[:-12]+'.'+str(val)[-12:]), 4)

    def get_current_hashrate(self):
        url = self.__get_miner_url()
        return self.__get_data(url)['hash']

    def get_avg_hashrate(self, avg_time_hours=6):
        url = '/'.join([self.base_url, 'miner', self.wallet, 'chart', 'hashrate'])
        data = self.__get_data(url)
        
        avg = []
        
        now = datetime.now() 
        for i in data:
            t = datetime.fromtimestamp(i['ts'] / 1e3)
            if now - t < timedelta(hours=avg_time_hours):
                avg.append(i['hs'])
            else:
                continue
        if len(avg) == 0:
            return 0
        else:
            return round(sum(avg) / float(len(avg)), 2)

    def get_difficulty(self):
        url = '/'.join([self.base_url, 'network', 'stats'])
        return self.__get_data(url)['difficulty'] / 10**6

    def get_aprox_earnings(self, poolfee=1.0):
        avg_hashrate = self.get_avg_hashrate()
        
        url = '/'.join([self.base_url, 'network', 'stats'])
        data = self.__get_data(url)
        difficulty = data['difficulty']
        block_reward = data['value']
        block_reward = float(str(block_reward)[:-12]+'.'+str(block_reward)[-12:])
        
        daily_reward = (avg_hashrate / difficulty) * block_reward * 86400 *(1.0 - poolfee/100.0)
#        weekly_reward = daily_reward * 7
        monthly_reward = daily_reward * 30
        return round(monthly_reward, 2)

    def get_time_until_payment(self, payment_limit=0.25):
        balance = self.get_balance()
        hourly_earning_rate = self.get_aprox_earnings() / 720
        hours_until_payment = (payment_limit - balance) / hourly_earning_rate
        if hours_until_payment < 0:
            return 0
        else:
            return round(hours_until_payment, 1)

    def get_coin_prices(self):
        url = 'https://api.coinmarketcap.com/v1/ticker/aeon/'
        return round(float(self.__get_data(url)[0]['price_usd']), 2)

    def __get_miner_url(self):
        return '/'.join([self.base_url, 'miner', self.wallet, 'stats'])        

    def __get_data(self, url):
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

        req = Request(url=url, headers=header)
        response = urlopen(req).read().decode("utf-8")

        data = json.loads(response)
        return data

if __name__ == '__main__':
    FUNCTION_MAP = ['balance',
                    'avg_hashrate',
                    'current_hashrate',
                    'aprox_earnings',
                    'coin_prices',
                    'difficulty',
                    'time_until_payment',
                    'total_payout']
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=FUNCTION_MAP)
    parser.add_argument('-w', '--wallet', type=str, help='wallet address', required=True)
    
    args = parser.parse_args()

    wallet = args.wallet
    
    aeon = AeonMiningPool(wallet)
    print(getattr(aeon, 'get_' + args.command)())