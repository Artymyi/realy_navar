import requests
import ast
import aiohttp
import asyncio
import time
import datetime


USDT = '0x55d398326f99059ff775485246999027b3197955'
dollars = 160
procent_navara = 2
now = datetime.datetime.now()
volume_navara = 100


def read_dict_from_file(namefile):
    with open(namefile) as f:
        text = f.read()
        d = ast.literal_eval(text)
    return d


def read_file(name_file):
    temp = []
    file = open(name_file, 'r')
    while True:
        line = file.readline()
        if not line:
            break
        temp.append(line.strip())
    file.close()
    temp.sort()
    return temp


async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy = "http://ZGMszS:ePb16p@91.188.242.35:9835") as resp:
            return await resp.json(content_type=None)

coins_add_dec_BITRUE = read_dict_from_file("dict_bitrue(18.06.22).txt")
coins_BITRUE_PANC = list(coins_add_dec_BITRUE.keys())
coins_BITRUE = [coins_BITRUE_PANC[i:i +20] for i in range(0, len(coins_BITRUE_PANC), 20)]

coins_add_dec_MEXC = read_dict_from_file("dict_mexc(19.06.2022).txt")
coins_MEXC_PANC = list(coins_add_dec_MEXC.keys())
coins_MEXC = [coins_MEXC_PANC[i:i + 15] for i in range(0, len(coins_MEXC_PANC), 15)]

coins_add_dec_KUCKOIN = read_dict_from_file("dict_kucoin(19.06.2022).txt")
coins_KUCKOIN_PANC = list(coins_add_dec_KUCKOIN.keys())
coins_KUCKOIN = [coins_KUCKOIN_PANC[i:i + 20] for i in range(0, len(coins_KUCKOIN_PANC), 20)]

coins_add_dec_BITMART = read_dict_from_file("dict_bitmart.txt")
coins_BITMART_PANC = list(coins_add_dec_BITMART.keys())
coins_BITMART = [coins_BITMART_PANC[i:i + 3] for i in range(0, len(coins_BITMART_PANC), 3)]

coins_add_dec_BKEX = read_dict_from_file("dict_BKEX.txt")
coins_BKEX_PANC = list(coins_add_dec_BKEX.keys())
coins_BKEX = [coins_BKEX_PANC[i:i + 20] for i in range(0, len(coins_BKEX_PANC), 20)]

coins_add_dec_Lbank = read_dict_from_file("dict_Lbank.txt")
coins_Lbank_PANC = list(coins_add_dec_Lbank.keys())
coins_Lbank = [coins_Lbank_PANC[i:i + 20] for i in range(0, len(coins_Lbank_PANC), 20)]

async def get_navar_bitrue(pid, arr, dict):
    average_price_sell, average_volume_sell = 0, 0
    try:
        res1 = await aiohttp_get(
            f"https://bsc.api.0x.org/swap/v1/quote?buyToken={dict[arr[pid]][1]}&sellToken={USDT}&sellAmount={int((10 ** 18) * (dollars))}")
        price_pancake = float(res1['sellAmount']) / float(res1['buyAmount']) * 10 ** (dict[arr[pid]][2] - 18)
        print(f'{arr[pid]} success parse from pancakeswap')


    except Exception as exc:
        print(exc)
        print(f'{arr[pid]} not parse from pancake')

    try:
        orders = await aiohttp_get(f"https://openapi.bitrue.com/api/v1/depth?symbol={arr[pid]}USDT&limit=5")
        for i in range(len(orders['bids'])):
            average_price_sell += float(orders['bids'][i][0])
            average_volume_sell += float(orders['bids'][i][1])
        average_price_sell /= len(orders['bids'])
        average_volume_sell /= len(orders['bids'])
        print(arr[pid], 'success parse from Bitrue')
    except:
        print(f'{arr[pid]} not parse from Bitrue API ORDERS')
    burn = dict[arr[pid]][3]

    try:
        if (average_price_sell / price_pancake - burn * 3 / 100) >= 1 + procent_navara / 100 and average_price_sell * average_volume_sell >= volume_navara:
            return (f'✅{now.strftime("%d-%m-%Y %H:%M")}\n'
                    f'<b>Coin</b> {arr[pid]}\n'
                    f'<b>Покупаем на</b> `{dict[arr[pid]][1]}`\n'
                    f'<b>Продаем на</b> https://www.bitrue.com/trade/{arr[pid].lower()}_usdt\n'
                    f'<b>Навар:</b> {(average_price_sell / price_pancake - 1) * 100:.3f} % \n'
                    f'<b>Средняя цена покупки pancake:</b> {price_pancake} $ \n'
                    f'<b>Средняя цена покупки:</b> {average_price_sell} $ \n'
                    f'<b>Средний объем покупки:</b> {average_volume_sell * average_price_sell:.3f} $')

    except:
        print(f'{arr[pid]} it doesnt count')

async def get_navar_mexc(pid, arr, dict):
    average_price_buy, average_volume_buy, average_price_sell, average_volume_sell = 0, 0, 0, 0
    try:
        res1 = await aiohttp_get(
            f"https://bsc.api.0x.org/swap/v1/quote?buyToken={dict[arr[pid]][1]}&sellToken={USDT}&sellAmount={int((10 ** 18) * (dollars))}")
        price_pancake = float(res1['sellAmount']) / float(res1['buyAmount']) * 10 ** (dict[arr[pid]][2] - 18)
        print(f'{arr[pid]} success parse from pancakeswap')
    except Exception as exc:
        print(f'{arr[pid]} not parse from pancake')
        print(exc)

    try:
        orders = await aiohttp_get(f"https://api.mexc.com/api/v3/depth?symbol={arr[pid]}USDT&limit=5")
        for j in range(len(orders['bids'])):
            average_price_sell += float(orders['bids'][j][0])
            average_volume_sell += float(orders['bids'][j][1])
        average_price_sell /= len(orders['bids'])
        average_volume_sell /= len(orders['bids'])
        print(arr[pid], 'success parse from Mexc')
    except:
        print(f'{arr[pid]} not parse from Mexc API ORDERS')
    burn = dict[arr[pid]][3]

    try:
        if (average_price_sell / price_pancake - burn * 3 / 100) >= 1 + procent_navara / 100 and average_price_sell * average_volume_sell >= volume_navara:
            return (f'✅{now.strftime("%d-%m-%Y %H:%M")}\n'
                    f'<b>Coin</b> {arr[pid]}\n'
                    f'<b>Покупаем на</b> `{dict[arr[pid]][1]}`\n'
                    f'<b>Продаем на</b> https://www.mexc.com/ru-RU/exchange/{arr[pid]}_USDT\n'
                    f'<b>Навар:</b> {(average_price_sell / price_pancake - 1) * 100:.3f} % \n'
                    f'<b>Средняя цена покупки pancake:</b> {price_pancake} $ \n'
                    f'<b>Средняя цена покупки:</b> {average_price_sell} $ \n'
                    f'<b>Средний объем покупки:</b> {average_volume_sell * average_price_sell:.3f} $')

    except Exception as exc:
        print(f'{arr[pid]} it doesnt count')
        print(exc)

async def get_navar_kuckoin(pid, arr, dict):
    average_price_buy, average_volume_buy, average_price_sell, average_volume_sell = 0, 0, 0, 0

    try:
        res1 = await aiohttp_get(
            f"https://bsc.api.0x.org/swap/v1/quote?buyToken={dict[arr[pid]][1]}&sellToken={USDT}&sellAmount={int((10 ** 18) * (dollars))}")
        price_pancake = float(res1['sellAmount']) / float(res1['buyAmount']) * 10 ** (dict[arr[pid]][2] - 18)
        print(f'{arr[pid]} success parse from pancakeswap')

    except Exception as exc:
        print(f'{arr[pid]} not parse from pancake')
        print(exc)
    try:
        orders = await aiohttp_get(f"https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol={arr[pid]}-USDT")
        for i in range(5):
            average_price_sell += float(orders['data']['bids'][i][0])
            average_volume_sell += float(orders['data']['bids'][i][1])
        average_price_sell /= 5
        average_volume_sell /= 5
        print('success parse Kucoin API ORDERS')
    except:
        print(f'{arr[pid]} not parse from Kucoin API ORDERS')

    burn = dict[arr[pid]][3]
    try:
        input_output = await aiohttp_get(f'https://api.kucoin.com/api/v1/currencies/{arr[pid]}')
        if input_output['data']['isWithdrawEnabled'] == True and input_output['data'][
            'isDepositEnabled'] == True:
            arbitrage = True
        else:
            arbitrage = False
    except:
        print(f'{arr[pid]} not parse from Kucoin INPUT-OUTPUT')

    try:
        if (
                average_price_sell / price_pancake - burn * 3 / 100) >= 1 + procent_navara / 100 and arbitrage == True and average_price_sell * average_volume_sell >= volume_navara:
            print('Est', f'✅{now.strftime("%d-%m-%Y %H:%M")}')
            return (f'✅{now.strftime("%d-%m-%Y %H:%M")}\n'
                    f'<b>Coin</b> {arr[pid]}\n'
                    f'<b>Покупаем на</b> `{dict[arr[pid]][1]}`\n'
                    f'<b>Продаем на</b>  https://www.kucoin.com/ru/trade/{arr[pid]}-USDT\n'
                    f'<b>Навар:</b> {(average_price_sell / price_pancake - 1) * 100:.3f} % \n'
                    f'<b>Средняя цена покупки pancake:</b> {price_pancake} $ \n'
                    f'<b>Средняя цена покупки:</b> {average_price_sell} $ \n'
                    f'<b>Средний объем покупки:</b> {average_volume_sell * average_price_sell:.3f} $')

    except:
        print(f'{arr[pid]} it doesnt count')

async def get_navar_bitmart(pid, arr, dict):
    average_price_sell, average_volume_sell = 0, 0
    try:
        res1 = await aiohttp_get(
            f"https://bsc.api.0x.org/swap/v1/quote?buyToken={dict[arr[pid]][1]}&sellToken={USDT}&sellAmount={int((10 ** 18) * (dollars))}")
        price_pancake = float(res1['sellAmount']) / float(res1['buyAmount']) * 10 ** (dict[arr[pid]][2] - 18)
        print(f'{arr[pid]} success parse from pancakeswap')
    except Exception as exc:
        print(f'{arr[pid]} not parse from pancake')
        print(exc)

    try:
        orders = await aiohttp_get(f"https://api-cloud.bitmart.com/spot/v1/symbols/book?symbol={arr[pid]}_USDT&size=5")
        for j in range(len(orders['data']['buys'])):
            average_price_sell += float(orders['data']['buys'][j]['price'])
            average_volume_sell += float(orders['data']['buys'][j]['amount'])
        average_price_sell /= len(orders['data']['buys'])
        average_volume_sell /= len(orders['data']['buys'])
        print('success parse Bitmart API ORDERS')
    except:
        print(f'{arr[pid]} not parse from Bitmart API ORDERS')
    burn = dict[arr[pid]][3]

    try:
        if (
                average_price_sell / price_pancake - burn * 3 / 100) >= 1 + procent_navara / 100 and average_price_sell * average_volume_sell >= volume_navara or  (price_pancake / average_price_sell - burn * 3 / 100) >= 1 + procent_navara / 100:
            return (f'✅{now.strftime("%d-%m-%Y %H:%M")}\n'
                    f'<b>Coin</b> {arr[pid]}\n'
                    f'<b>Покупаем на</b> `{dict[arr[pid]][1]}`\n'
                    f'<b>Продаем на</b>  https://www.bitmart.com/trade/en?symbol={arr[pid]}_USDT\n'
                    f'<b>Навар:</b> {(average_price_sell / price_pancake - 1) * 100:.3f} % \n'
                    f'<b>Средняя цена покупки pancake:</b> {price_pancake} $ \n'
                    f'<b>Средняя цена покупки:</b> {average_price_sell} $ \n'
                    f'<b>Средний объем покупки:</b> {average_volume_sell * average_price_sell:.3f} $')

    except:
        print(f'{arr[pid]} it doesnt count')

async def get_navar_BKEX(pid, arr, dict):
    average_price_buy, average_volume_buy, average_price_sell, average_volume_sell = 0, 0, 0, 0
    try:
        res1 = await aiohttp_get(
            f"https://bsc.api.0x.org/swap/v1/quote?buyToken={dict[arr[pid]][1]}&sellToken={USDT}&sellAmount={int((10 ** 18) * (dollars))}")
        price_pancake = float(res1['sellAmount']) / float(res1['buyAmount']) * 10 ** (dict[arr[pid]][2] - 18)
        print(f'{arr[pid]} success parse from pancakeswap')
    except Exception as exc:
        print(f'{arr[pid]} not parse from pancake')
        print(exc)
    try:
        orders = await aiohttp_get(f"https://api.bkex.com/v2/q/depth?symbol={arr[pid]}_USDT&depth=5")
        for j in range(len(orders["data"]["bid"])):
            average_price_sell += float(orders["data"]["bid"][j][0])
            average_volume_sell += float(orders["data"]["bid"][j][1])
        average_price_sell /= len(orders["data"]["bid"])
        average_volume_sell /= len(orders["data"]["bid"])
        print('success parse Bkex API ORDERS')
    except Exception as exc:
        print(f'{arr[pid]} not parse from BKEX API ORDERS')
        print(exc)
    burn = dict[arr[pid]][3]

    try:
        if (average_price_sell / price_pancake - burn * 3 / 100) >= 1 + procent_navara / 100 and average_price_sell * average_volume_sell >= volume_navara:
            return (f'✅{now.strftime("%d-%m-%Y %H:%M")}\n'
                    f'<b>Coin</b> {arr[pid]}\n'
                    f'<b>Покупаем на</b> `{dict[arr[pid]][1]}`\n'
                    f'<b>Продаем на</b> https://www.bkex.com/trade/{arr[pid]}_USDT\n'
                    f'<b>Навар:</b> {(average_price_sell / price_pancake - 1) * 100:.3f} % \n'
                    f'<b>Средняя цена покупки pancake:</b> {price_pancake} $ \n'
                    f'<b>Средняя цена покупки:</b> {average_price_sell} $ \n'
                    f'<b>Средний объем покупки:</b> {average_volume_sell * average_price_sell:.3f} $')

    except:
        print(f'{arr[pid]} it doesnt count')

async def get_navar_Lbank(pid, arr, dict):
    average_price_buy, average_volume_buy, average_price_sell, average_volume_sell = 0, 0, 0, 0
    try:
        res1 = await aiohttp_get(
            f"https://bsc.api.0x.org/swap/v1/quote?buyToken={dict[arr[pid]][1]}&sellToken={USDT}&sellAmount={int((10 ** 18) * (dollars))}")
        price_pancake = float(res1['sellAmount']) / float(res1['buyAmount']) * 10 ** (dict[arr[pid]][2] - 18)
        print(f'{arr[pid]} success parse from pancakeswap')
    except Exception as exc:
        print(f'{arr[pid]} not parse from pancake')
        print(exc)

    try:
        orders = await aiohttp_get(f"https://api.lbkex.com/v2/depth.do?symbol={arr[pid].lower()}_usdt&size=5")
        for j in range(len(orders['data']['bids'])):
            average_price_sell += float(orders['data']['bids'][j][0])
            average_volume_sell += float(orders['data']['bids'][j][1])
        average_price_sell /= len(orders['data']['bids'])
        average_volume_sell /= len(orders['data']['bids'])
        print(arr[pid], 'success parse from Mexc')
    except:
        print(f'{arr[pid]} not parse from Mexc API ORDERS')
    burn = dict[arr[pid]][3]

    try:
        if (average_price_sell / price_pancake - burn * 3 / 100) >= 1 + procent_navara / 100 and average_price_sell * average_volume_sell >= volume_navara:
            return (f'✅{now.strftime("%d-%m-%Y %H:%M")}\n'
                    f'<b>Coin</b> {arr[pid]}\n'
                    f'<b>Покупаем на</b> `{dict[arr[pid]][1]}`\n'
                    f'<b>Продаем на</b> https://www.lbank.info/exchange/{arr[pid].lower()}/usdt\n'
                    f'<b>Навар:</b> {(average_price_sell / price_pancake - 1) * 100:.3f} % \n'
                    f'<b>Средняя цена покупки pancake:</b> {price_pancake} $ \n'
                    f'<b>Средняя цена покупки:</b> {average_price_sell} $ \n'
                    f'<b>Средний объем покупки:</b> {average_volume_sell * average_price_sell:.3f} $')

    except Exception as exc:
        print(f'{arr[pid]} it doesnt count')
        print(exc)


async def main_BITRUE(x):
    futures = [get_navar_bitrue(i, x, coins_add_dec_BITRUE) for i in range(len(x))]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if result != None:
            requests.get(
                f'https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text={result}&parse_mode=html')

async def main_MEXC(x):
    futures = [get_navar_mexc(i, x, coins_add_dec_MEXC) for i in range(len(x))]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if result != None:
            requests.get(
                f'https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text={result}&parse_mode=html')

async def main_KUCKOIN(x):
    futures = [get_navar_kuckoin(i, x, coins_add_dec_KUCKOIN) for i in range(len(x))]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if result != None:
            requests.get(
                f'https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text={result}&parse_mode=html')

async def main_BITMART(x):
    futures = [get_navar_bitmart(i, x, coins_add_dec_BITMART) for i in range(len(x))]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if result != None:
            requests.get(
                f'https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text={result}&parse_mode=html')

async def main_BKEX(x):
    futures = [get_navar_BKEX(i, x, coins_add_dec_BKEX) for i in range(len(x))]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if result != None:
            requests.get(
                f'https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text={result}&parse_mode=html')

async def main_Lbank(x):
    futures = [get_navar_Lbank(i, x, coins_add_dec_Lbank) for i in range(len(x))]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if result != None:
            requests.get(
                f'https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text={result}&parse_mode=html')

while True:

   start = time.time()
   # for i in range(0, len(coins_BITRUE)):
   #     asyncio.get_event_loop().run_until_complete(main_BITRUE(coins_BITRUE[i]))
   # print("Process took: {:.2f} seconds".format(time.time() - start))

   # for i in range(0, len(coins_MEXC)):
   #     asyncio.get_event_loop().run_until_complete(main_MEXC(coins_MEXC[i]))
   # print("Process took: {:.2f} seconds".format(time.time() - start))

   # for i in range(0, len(coins_KUCKOIN)):
   #     asyncio.get_event_loop().run_until_complete(main_KUCKOIN(coins_KUCKOIN[i]))
   # print("Process took: {:.2f} seconds".format(time.time() - start))

   # for i in range(0, len(coins_BITMART)):
   #     asyncio.get_event_loop().run_until_complete(main_BITMART(coins_BITMART[i]))
   # print("Process took: {:.2f} seconds".format(time.time() - start))

   # for i in range(0, len(coins_BKEX)):
   #     asyncio.get_event_loop().run_until_complete(main_BKEX(coins_BKEX[i]))
   # print("Process took: {:.2f} seconds".format(time.time() - start))

   # for i in range(0, len(coins_Lbank)):
   #     asyncio.get_event_loop().run_until_complete(main_Lbank(coins_Lbank[i]))
   # print("Process took: {:.2f} seconds".format(time.time() - start))

   # requests.get('https://api.telegram.org/bot5209914651:AAEN-hCUNErgAztvSZGOHktY_2WEnLCjAxs/sendMessage?chat_id=-1001617784887&text=Цикл закончился {:.2f}&parse_mode=html'.format(time.time() - start))
   time.sleep(60)

