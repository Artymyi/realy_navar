import requests
import json
import time

# bitrue
#------------------------------------------------

# coins_bitrue = []
# no_symbols = ['3S', '3L']
# result = requests.get(url="https://openapi.bitrue.com/api/v1/ticker/24hr")
# result_obj = json.loads(result.text)
# for i in range(len(result_obj)):
#     flag = True
#     if 'USDT' in result_obj[i]['symbol']:
#         for j in range(len(no_symbols)):
#             if no_symbols[j] in result_obj[i]['symbol']:
#                 flag = False
#                 break
#         if flag == True:
#             coins_bitrue.append(result_obj[i]['symbol'].replace('USDT', '').lower())
# # len coins_bitrue = 753
#
# result_1 = requests.get(url="https://openapi.bitrue.com/api/v1/exchangeInfo")
# result_1_obj = json.loads(result_1.text)
#
# coins_usdt_bsc = []
#
# # метамарфоза списка словарей в словарь словарей
# dict = {}
# for i in range(len(result_1_obj['coins'])):
#     dict.update({result_1_obj['coins'][i]["coin"]: result_1_obj['coins'][i]})
#
# f = open('bitrue_new', "w")
# for i in range(len(coins_bitrue)):
#     if coins_bitrue[i] in list(dict.keys()):
#         if 'BEP20' in dict[f'{coins_bitrue[i]}']["chains"]:
#                 coins_usdt_bsc.append(coins_bitrue[i])
#                 f.write(f'{coins_bitrue[i]}, ')
#
# print(type(dict['ada']['chainDetail'][0]['enableWithdraw']))
# print(type(dict['ada']['chainDetail'][0]['enableDeposit']))
#
# # # print(coins_bitrue)
# # # print(list(dict.keys()))
# # print(len(coins_usdt_bsc))

# --------------------------------------

# mexc
# coins_usdt_mexc= []
# coins_usdt_bsc_mexc = []
# result = requests.get(url="https://www.mexc.com/open/api/v2/market/symbols")
# result_obj = json.loads(result.text)
# dict = {}
# for i in range(len(result_obj['data'])):
#     dict.update({result_obj['data'][i]['symbol']: result_obj['data'][i]})
# for key in dict:
#     if 'USDT' in key:
#         coins_usdt_mexc.append(key.replace('_USDT', ''))
# print(coins_usdt_mexc)
# print(len(coins_usdt_mexc))
#
# result1 = requests.get(url="https://www.mexc.com/open/api/v2/market/coin/list")
# result_obj1 = json.loads(result1.text)
# file = open('mexc_coins_new.txt', 'w')
# for i in range(len(result_obj1['data'])):
#     if result_obj1['data'][i]['currency'] in coins_usdt_mexc:
#         if result_obj1['data'][i]['coins'][0]['chain'] == 'BEP20(BSC)' or result_obj1['data'][i]['coins'][0]['chain'] == 'BSC' or result_obj1['data'][i]['coins'][0]['chain'] == 'BEP20':
#             coins_usdt_bsc_mexc.append(result_obj1['data'][i]['currency'])
# for i in range(len(coins_usdt_bsc_mexc)):
#     file.write(f'{coins_usdt_bsc_mexc[i]}, ')
#
# print(len(coins_usdt_bsc_mexc))

#--------------------------------------------

# kucoin
# coins_usdt_kucoin = []
# coins_usdt_bsc_kucoin = []
# result = requests.get(url="https://api.kucoin.com/api/v1/symbols")
# result_obj = json.loads(result.text)
# dict = {}
# for i in range(len(result_obj['data'])):
#     dict.update({result_obj['data'][i]['symbol']: result_obj['data'][i]})
# for key in dict:
#     if 'USDT' in key:
#         coins_usdt_kucoin.append(key.replace('-USDT', ''))
# print(len(coins_usdt_kucoin))
#
# for i in range(len(coins_usdt_kucoin)):
#     result1 = requests.get(url=f"https://api.kucoin.com/api/v2/currencies/{coins_usdt_kucoin[i]}")
#     result_obj1 = json.loads(result1.text)
#     try:
#         for j in range(len(result_obj1['data']['chains'])):
#             if result_obj1['data']['chains'][j]['chainName'] == 'BEP20':
#                 coins_usdt_bsc_kucoin.append(coins_usdt_kucoin[i])
#                 break
#     except:
#         print(coins_usdt_kucoin[i])

# file = open('kucoin_coins_new.txt', 'w')
# for i in range(len(coins_usdt_bsc_kucoin)):
#     file.write(f'{coins_usdt_bsc_kucoin[i]}, ')
# file.close()
# print(len(coins_usdt_bsc_kucoin))


#------------------------------------------
# bitmart

# coins_usdt_bitmart = []
# coins_usdt_bsc_bitmart = []
# result = requests.get(url="https://api-cloud.bitmart.com/spot/v1/symbols")
# result_obj = json.loads(result.text)
# print(result_obj['data']['symbols'])
# for i in range(len(result_obj['data']['symbols'])):
#     if "USDT" in result_obj['data']['symbols'][i]:
#         coins_usdt_bitmart.append(result_obj['data']['symbols'][i].replace('_USDT', ''))
# print(len(coins_usdt_bitmart))

# dict = {}
# for i in range(len(result_obj['data']['symbols'])):
#     dict.update({result_obj['data'][i]['symbol']: result_obj['data'][i]})
# for key in dict:
#     if 'USDT' in key:
#         coins_usdt_kucoin.append(key.replace('-USDT', ''))
# print(len(coins_usdt_kucoin))
# #
# for i in range(len(coins_usdt_kucoin)):
#     result1 = requests.get(url=f"https://api.kucoin.com/api/v2/currencies/{coins_usdt_kucoin[i]}")
#     result_obj1 = json.loads(result1.text)
#     try:
#         for j in range(len(result_obj1['data']['chains'])):
#             if result_obj1['data']['chains'][j]['chainName'] == 'BEP20':
#                 coins_usdt_bsc_kucoin.append(coins_usdt_kucoin[i])
#                 break
#     except:
#         print(coins_usdt_kucoin[i])

# file = open('kucoin_coins_new.txt', 'w')
# for i in range(len(coins_usdt_bsc_kucoin)):
#     file.write(f'{coins_usdt_bsc_kucoin[i]}, ')
# file.close()
# print(len(coins_usdt_bsc_kucoin))


# --------------------------------


coins_usdt_lbank = []
coins_usdt_bsc_lbank = []
result = requests.get(url="https://api.lbkex.com/v2/currencyPairs.do")
result_obj = json.loads(result.text)
print(result_obj['data'])
for i in range(len(result_obj['data'])):
    if "usdt" in result_obj['data'][i]:
        coins_usdt_lbank.append(result_obj['data'][i].replace('_usdt', '').upper())

file = open('lbank_coins.txt', 'w')
for i in range(len(coins_usdt_lbank)):
    file.write(f'{coins_usdt_lbank[i]}, ')
file.close()

# dict = {}
# for i in range(len(result_1_obj['coins'])):
#     dict.update({result_1_obj['coins'][i]["coin"]: result_1_obj['coins'][i]})




