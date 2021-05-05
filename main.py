import requests
import time
import logging
from forex_python.converter import CurrencyRates

api_key = 'bff68f59-ffc2-4162-8b03-0ba2bd0e65bb'
bot_token = '1765338910:AAFvFMvnmMHwGqSDw0QfGVFYZYZiuaSTSCA'
currency_key = 'c7253cea36d9cc9427e589cc3076663e'

c = CurrencyRates()
inr = c.get_rate('USD', 'INR')
chat_id = '936345588'
eth_threshold = 3250  # 2000
doge_threshold = 0.60  # 0.3
btc_threshold = 55500  # 55000
time_interval = 2 * 60  # in seconds

btc_sell_min = 4655000
btc_sell_max = 4700000
eth_sell = 220000
doge_sell = 33

def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    btc_price = response_json['data'][0]
    btc_per_change = btc_price['quote']['USD']['percent_change_24h']
    btc_price_ch = btc_price['quote']['USD']['price']
    #print(btc_per_change)
    btc_list = [btc_per_change,btc_price_ch]
    return btc_list #btc_price['quote']['USD']['price']


def get_eth_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    eth_price = response_json['data'][1]
    eth_per_change = eth_price['quote']['USD']['percent_change_24h']
    eth_price_ch = eth_price['quote']['USD']['price']
    eth_list = [eth_per_change,eth_price_ch]
    return eth_list #eth_price['quote']['USD']['price']


def get_doge_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    doge_price = response_json['data'][3]
    doge_per_change = doge_price['quote']['USD']['percent_change_24h']
    doge_price_ch = doge_price['quote']['USD']['price']
    doge_list = [doge_per_change, doge_price_ch]
    return doge_list #doge_price['quote']['USD']['price']


def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
    requests.get(url)


def main():
    btc_price_list = []
    eth_price_list = []
    doge_price_list = []
    while True:
        btc = get_btc_price()
        eth = get_eth_price()
        doge = get_doge_price()
        btc_price = round(btc[1])
        eth_price = round(eth[1])
        doge_price = doge[1]

        btc_inr_price = round(btc_price * inr)
        btc_price_list.append(btc_inr_price)

        eth_inr_price = round(eth_price * inr)
        eth_price_list.append(eth_inr_price)

        doge_inr_price = round(doge_price * inr)
        doge_price_list.append(doge_inr_price)

        if btc[0]<0:
            btc_value = f"Percentage Change ⬇ {btc[0]}"
        else:
            btc_value = f"Percentage Change ⬆ {btc[0]}"

        if eth[0]<0:
            eth_value = f"Percentage Change ⬇ {eth[0]}"
        else:
            eth_value = f"Percentage Change ⬆ {eth[0]}"

        if doge[0]<0:
            doge_value = f"Percentage Change ⬇ {doge[0]}"
        else:
            doge_value = f"Percentage Change ⬆ {doge[0]}"

        if btc_price < btc_threshold:
            send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: USD:{btc_price} | INR:{btc_inr_price} | {btc_value}')
        if len(btc_price_list) >= 6:
            send_message(chat_id=chat_id, msg=btc_price_list + "time:" + last_updated)
            btc_price_list = []

        if eth_price < eth_threshold:
            send_message(chat_id=chat_id, msg=f'ETH Price Drop Alert: USD:{eth_price} | INR:{eth_inr_price} | {eth_value}')
        if len(eth_price_list) >= 6:
            send_message(chat_id=chat_id, msg=eth_price_list + "time:" + last_updated)
            eth_price_list = []

        if doge_price < doge_threshold:
            send_message(chat_id=chat_id, msg=f'DogeCoin Price Drop Alert: USD:{doge_price} | INR:{doge_inr_price} | {doge_value}')
        if len(doge_price_list) >= 6:
            send_message(chat_id=chat_id, msg=doge_price_list + "time:" + last_updated)
            doge_price_list = []

        if btc_sell_min<btc_inr_price and btc_sell_max>btc_inr_price:
            send_message(chat_id=chat_id, msg=f'Sell BTC Price UP ⬆: INR:{btc_inr_price} ')

        time.sleep(time_interval)


if __name__ == "__main__":
    main()
