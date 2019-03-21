import json
import time
import requests
from etherscan import accounts, tokens

#Use of Etherscan API to pull wallet balances
#Initialize function with your API key and address

twentyFourHours = 86400
address = '0x010589B7c33034b802F7dbA2C88cc9cec0f46673' #Address to interact with to mint more SOV
api_key = 'IVPR3T2CWJ2TKUYH6824HNGKKJ4ENEM9EU'

#Function to populate a list with transactions for the last 24 hours. 
#Can be called to refresh a list in case of some error. Returns a list
def init_sov_24_hours():

    api = accounts.Account(address=address, api_key=api_key)
    transactions_24_hours = api.get_transaction_page(offset=10000)

    i = len(transactions_24_hours)    
    latest_24_hours = (int(transactions_24_hours[i - 1]['timeStamp']) - twentyFourHours)

    k = 0
    while (int(transactions_24_hours[k]['timeStamp'])) < latest_24_hours:
        k += 1
    
    transactionsList = []
    while k < len(transactions_24_hours):
        transactionsList.append(k)
        k += 1

    return transactionsList

#Function to update list received from init_sov_24_hours(). This function should be used to 
#update the list stored in order to reduce large API calls and to improve performance.
#Takes the latest 5 transctions, as described in offset param in update variable
def update_sov_24_hours(transactions):

    api = accounts.Account(address=address, api_key=api_key)
    update = api.get_transaction_page(page=1, offset=5)

    k = 0
    while (k < 5):
        if (update[k] == transactions[len(transactions) - k]):
            k += 1
        else:
            transactions.append(update[k])
            transactions.pop(0)
    
    return transactions

#Takes the last 24 hours list as input to find the average gas price paid, 
#Number of transactions, and number of SOV minted. Returns all values in a list
def gasAndNoOfTransactions(transactions):
    gasAggregate = 0

    k = 0
    while (k < len(transactions)):
        gasAggregate += int(transactions[k]['gasPrice']) 
        k += 1

    gasAverage = gasAggregate / k
    result = [gasAverage, k, k * 0.05] #average gas price paid, number of transactions, number of SOV minted

    return result

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

#Percent of total supply mined
def percent_mined():
    maxSupply = 21000000
    currentSupply = total_sov()
    percent = currentSupply / maxSupply

    return percent
