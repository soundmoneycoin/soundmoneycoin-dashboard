import json
import time
import requests
from etherscan import accounts, tokens

#Use of Etherscan API to pull wallet balances
#Initialize function with your API key and address


twentyFourHours = 86400
address = '0x010589B7c33034b802F7dbA2C88cc9cec0f46673'
api_key = 'IVPR3T2CWJ2TKUYH6824HNGKKJ4ENEM9EU'

#Total amount of SOV in circulation
def total_sov():
    api = tokens.Tokens(contract_address=address, api_key=api_key)
    total = api.get_total_supply()
    return (int(total) / 100000000)

#latest gas price paid for minting 1 SOV coin
def latest_avg():
    api = accounts.Account(address=address, api_key=api_key)
    avg = api.get_transaction_page(page=1)
    latest = avg[1]['gasPrice']
    return latest

#function to receive average gas price paid in last 24 hours and number of transactions in last 24 hours
#A return value of 10000 for transactions most likely means there are more than 10000 transactions
def sov_24_hours():
    #minted = "http://api.etherscan.io/api?module=account&action=txlist&address=" + address + "&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key
    #req = requests.get(minted)
    #reqJ = req.json()

    api = accounts.Account(address=address, api_key=api_key)
    transactions_24_hours = api.get_transaction_page(offset=10000)

    counter = 0
    gasAggregate = 0
    
    latest_24_hours = (int(transactions_24_hours[0]['timeStamp']) - twentyFourHours)

    i = 0
    while (int(transactions_24_hours[i]['timeStamp'])) < latest_24_hours:
        i += 1
    
    while i < len(transactions_24_hours):
        gasAggregate += int(transactions_24_hours[i]['gasPrice']) 
        i += 1
        counter += 1

    gasAverage = gasAggregate / counter
    result = [gasAverage, counter]

    return result
    
x = sov_24_hours()
print (x)



