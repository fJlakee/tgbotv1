from telegram.ext import Updater, CommandHandler
import logging
import ccxt
import time
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

currency_pairs = ['BTC/USDT', 'ETH/USDT', 'NEO/USDT', 'LTC/USDT', 'QTUM/USDT', 'ADA/USDT', 'XRP/USDT', 'EOS/USDT', 'IOTA/USDT', 'XLM/USDT', 'ONT/USDT', 'TRX/USDT', 'ETC/USDT', 'ICX/USDT', 'NULS/USDT', 'VET/USDT', 'USDC/USDT', 'LINK/USDT', 'WAVES/USDT', 'ONG/USDT', 'ZIL/USDT', 'ZRX/USDT', 'FET/USDT', 'BAT/USDT', 'XMR/USDT', 'ZEC/USDT', 'CELR/USDT', 'DASH/USDT', 'OMG/USDT', 'THETA/USDT', 'ENJ/USDT', 'MATIC/USDT', 'ATOM/USDT', 'TFUEL/USDT', 'ONE/USDT', 'FTM/USDT', 'ALGO/USDT', 'DOGE/USDT', 'DUSK/USDT', 'ANKR/USDT', 'MTL/USDT', 'DOCK/USDT', 'WAN/USDT', 'CVC/USDT', 'CHZ/USDT', 'BAND/USDT', 'XTZ/USDT', 'REN/USDT', 'RVN/USDT', 'HBAR/USDT', 'NKN/USDT', 'STX/USDT', 'KAVA/USDT', 'ARPA/USDT', 'IOTX/USDT', 'RLC/USDT', 'CTXC/USDT', 'BCH/USDT', 'VITE/USDT', 'FTT/USDT', 'EUR/USDT', 'OGN/USDT', 'DREP/USDT', 'WRX/USDT', 'LSK/USDT', 'BNT/USDT', 'LTO/USDT', 'COTI/USDT', 'STPT/USDT', 'DATA/USDT', 'SOL/USDT', 'CTSI/USDT', 'HIVE/USDT', 'CHR/USDT', 'BTCUP/USDT', 'ARDR/USDT', 'MDT/USDT', 'KNC/USDT', 'LRC/USDT', 'PNT/USDT', 'COMP/USDT', 'ZEN/USDT', 'SNX/USDT', 'ETHUP/USDT', 'ETHDOWN/USDT', 'SXP/USDT', 'MKR/USDT', 'DCR/USDT', 'STORJ/USDT', 'BNBUP/USDT', 'MANA/USDT', 'YFI/USDT', 'BAL/USDT', 'BLZ/USDT', 'IRIS/USDT', 'KMD/USDT', 'JST/USDT', 'ANT/USDT', 'CRV/USDT', 'SAND/USDT', 'OCEAN/USDT', 'NMR/USDT', 'DOT/USDT', 'LUNA/USDT', 'PAXG/USDT', 'WNXM/USDT', 'TRB/USDT', 'SUSHI/USDT', 'KSM/USDT', 'EGLD/USDT', 'DIA/USDT', 'RUNE/USDT', 'FIO/USDT', 'UMA/USDT', 'BEL/USDT', 'WING/USDT', 'UNI/USDT', 'OXT/USDT', 'AVAX/USDT', 'FLM/USDT', 'ORN/USDT', 'UTK/USDT', 'XVS/USDT', 'ALPHA/USDT'] 

bybit = ccxt.bybit({
    'apiKey': 'aVCrSjIeu96OWktRRp',
    'secret': 'PVmeieYaY8NIBsVR0z29PIju0xdxFU6gpLUu',
})
binance = ccxt.binance({
    'apiKey': '07UoOw1aTntdQTCfODSdNAXeQbzHNrO0n2tOCn2GaR06IzlrIjuvfyQitd8szZfz',
    'secret': 'UA2wjr0C9Xd4FiGzaaDnVYpyOac2sxajHGdEgz98FJk1vsKqIbFuWMqK6fsh98sL',
})
kucoin = ccxt.kucoin({
    'password': 'IluN!029!2004115',
    'apiKey': '65a66147bba0820001281678',
    'secret': '9eced606-a065-4d27-8bb0-491d088ec3e0',
    'passphrase': 'IluN!029!2004115',
})
kraken = ccxt.kraken({
    'apiKey': '0TzkxY4PbDYv9ZT5A8z1B/FnLqUvo71rT7V1EPfRWZ3Q61kB20j8Dw8+',
    'secret': 'vcOtwBEQRpk8nYGXiNGbowKI1WHinNBcsTHtTQ6GfowPZjjIUho+xAMe662KccKmPANzfeY/hgOGJSNzesPYSw==',
})
mexc = ccxt.mexc({
    'apiKey': 'mx0vgltI9XTYdMtznN',
    'secret': '894ff80d2fd048b0ba55339fada3c38b',
})
huobi = ccxt.huobi({
    'apiKey': 'ntmuw4rrsr-0b39635b-fde68b30-6de2c',
    'secret': '96d8ec7a-01763cc3-c13ef582-2dcae',
})

exchanges = [binance, bybit, kucoin, huobi, mexc]

min_spread = 1.01

#FORMAT: [[network, fee, withdrawEnable, depositEnable]]
def Binance_get_info(currency_code):
    try:
        main_info = binance.fetch_deposit_withdraw_fee(currency_code)
    except Exception as e:
        return 0
    networks_and_fees = {}
    counter = 0
    for i in main_info.get('networks'):
        if dict(main_info.get('info').get('networkList')[counter]).get('withdrawEnable') == True and dict(main_info.get('info').get('networkList')[counter]).get('depositEnable') == True:
            networks_and_fees.update({i : format(main_info.get('networks').get(i).get('withdraw').get('fee'), '.6f')})
        counter += 1
    return networks_and_fees

def KuCoin_get_info(currency_code):
    try:
        main_info = kucoin.fetch_deposit_withdraw_fee(currency_code)
    except Exception as e:
        return 0
    networks_and_fees = {}
    if main_info.get('info').get('isWithdrawEnabled') == True:
        for i in main_info.get('networks'):
            networks_and_fees.update({i: format(main_info.get('networks').get(i).get('withdraw').get('fee'), '.6f')})
    return networks_and_fees

def Mexc_get_info(currency_code):
    try:
        main_info = mexc.fetch_deposit_withdraw_fee(currency_code)
    except Exception as e:
        return 0
    networks_and_fees = {}
    counter = 0
    for i in main_info.get('networks'):
        if dict(main_info.get('info').get('networkList')[counter]).get('withdrawEnable') == True and dict(main_info.get('info').get('networkList')[counter]).get('depositEnable') == True:
            if "(" in str(i) and ")" in str(i):
                networks_and_fees.update({i[i.index("(") + 1:i.index(")")] : format(main_info.get('networks').get(i).get('withdraw').get('fee'), '.6f')})
            else:
                networks_and_fees.update({i : format(main_info.get('networks').get(i).get('withdraw').get('fee'), '.6f')})
        counter += 1
    return networks_and_fees

def Exchange_get_info(currency_code, exchange):
    try:
        main_info = exchange.fetch_deposit_withdraw_fee(currency_code)
    except Exception as e:
        print(e)
        return 0
    networks_and_fees = {}
    for i in main_info.get('info').get('chains'):
        if i.get('chainWithdraw') == "1" and i.get('chainDeposit') == "1":
            networks_and_fees.update({i.get('chain') : format(float(i.get('withdrawFee')), '.6f')})
    return networks_and_fees

def write_prime_data():
    prime_data = {}
    for pair in currency_pairs:
        currency_code = pair[:pair.index("/")]
        for i in range(0, len(exchanges) - 1):
            exchange_1 = exchanges[i]
            try:
                price_1 = exchange_1.fetch_ticker(pair)["ask"]
            except Exception as e:
                continue
            for j in range(0, len(exchanges)):
                if i == j : continue
                exchange_2 = exchanges[j]
                try:
                    price_2 = exchange_2.fetch_ticker(pair)["bid"]
                except Exception as e:
                    continue
                match exchange_1.id:
                    case "binance":
                        first_exchange_info = Binance_get_info(currency_code)
                    case "kucoin":
                        first_exchange_info = KuCoin_get_info(currency_code)
                    case "mexc":
                        first_exchange_info = Mexc_get_info(currency_code)
                    case _ :
                        first_exchange_info = Exchange_get_info(currency_code, exchange_1)
                match exchange_2.id:
                    case "binance":
                        second_exchange_info = Binance_get_info(currency_code)
                    case "kucoin":
                        second_exchange_info = KuCoin_get_info(currency_code)
                    case "mexc":
                        first_exchange_info = Mexc_get_info(currency_code)
                    case _ :
                        second_exchange_info = Exchange_get_info(currency_code, exchange_2)

                if first_exchange_info == {} or second_exchange_info == {} or first_exchange_info == 0 or second_exchange_info == 0:
                    continue
                common_networks = list(set(first_exchange_info).intersection(set(second_exchange_info)))
                common_networks = [str(element) for element in common_networks]
                if len(common_networks) != 0:
                    for a in common_networks:
                        if price_1 / price_2 >= min_spread:
                            prime_data.update({f"{exchange_1.id} to {exchange_2.id} with {pair} on {a}" : f"spread:{round(float(price_1 / price_2), 3)}/ fee: {round(float(first_exchange_info.get(a)) * float(price_1), 3)}$"})
                        elif price_2 / price_1 >= min_spread:
                            prime_data.update({f"{exchange_2.id} to {exchange_1.id} with {pair} on {a}" : f"spread:{round(float(price_2 / price_1), 3)}/ fee: {round(float(first_exchange_info.get(a)) * float(price_2), 3)}$"})
    if prime_data == {}:
        write_prime_data()
    else:
        with open("spreads.json", "w") as f:
            json.dump(prime_data, f)

def check_spread_change(new_data):
    messages_string = ""
    with open("spreads.json", "r+") as f:
        data = json.load(f)
    for i in data:
        try:
            if min_spread <= float(new_data[i][new_data[i].index(":") + 1 : new_data[i].index("/")]):
                messages_string += f"{i} : {new_data[i]}\n"
        except Exception as e:
            continue
    data.update(new_data)
    with open("spreads.json", "w") as f:
        json.dump(data, f)
    return messages_string


def get_new_data(update, context):
    new_data = {}
    for pair in currency_pairs:
        currency_code = pair[:pair.index("/")]
        for i in range(0, len(exchanges) - 1):
            exchange_1 = exchanges[i]
            try:
                price_1 = exchange_1.fetch_ticker(pair)["ask"]
            except Exception as e:
                continue
            for j in range(0, len(exchanges)):
                if i == j : continue
                exchange_2 = exchanges[j]
                try:
                    price_2 = exchange_2.fetch_ticker(pair)["bid"]
                except Exception as e:
                    continue
                match exchange_1.id:
                    case "binance":
                        first_exchange_info = Binance_get_info(currency_code)
                    case "kucoin":
                        first_exchange_info = KuCoin_get_info(currency_code)
                    case "mexc":
                        first_exchange_info = Mexc_get_info(currency_code)
                    case _ :
                        first_exchange_info = Exchange_get_info(currency_code, exchange_1)
                match exchange_2.id:
                    case "binance":
                        second_exchange_info = Binance_get_info(currency_code)
                    case "kucoin":
                        second_exchange_info = KuCoin_get_info(currency_code)
                    case "mexc":
                        second_exchange_info = Mexc_get_info(currency_code)
                    case _ :
                        second_exchange_info = Exchange_get_info(currency_code, exchange_2)
                if first_exchange_info == {} or second_exchange_info == {} or first_exchange_info == 0 or second_exchange_info == 0:
                    continue
                common_networks = list(set(first_exchange_info).intersection(set(second_exchange_info)))
                common_networks = [str(element) for element in common_networks]
                if len(common_networks) != 0:
                    for a in common_networks:
                        if price_1 / price_2 >= min_spread:
                            new_data.update({f"{exchange_1.id} to {exchange_2.id} with {pair} on {a}" : f"spread:{round(float(price_1 / price_2), 3)}/ fee: {round(float(first_exchange_info.get(a)) * float(price_1), 3)}$"})
                        elif price_2 / price_1 >= min_spread:
                            new_data.update({f"{exchange_2.id} to {exchange_1.id} with {pair} on {a}" : f"spread:{round(float(price_2 / price_1), 3)}/ fee: {round(float(first_exchange_info.get(a)) * float(price_2), 3)}$"})
    if new_data == {}:
        write_prime_data()
    else:
        message_to_bot = check_spread_change(new_data)
        try:
            context.bot.send_message(chat_id=update.message.chat_id, text=message_to_bot)
        except:
            print("Message_to_bot is probably empty", "\n")

def start(update, context):  
    update.message.reply_text('Проверяю цены...')
    while True:
        get_new_data(update, context)

def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token='6536148374:AAFKcnC8QZdLBsvPQojBR9kz-Or-WQDEvu0')
    dispatcher = updater.dispatcher    
    write_prime_data()
    start
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()