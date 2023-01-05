import concurrent.futures
import json
from web3 import Web3, exceptions
import os
import sys
import time


def resource_path(relative_path):
    """This function is for the path of additional files for tkinter"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


with open("./data/abis.json") as file:
    """Using the abi's"""
    w3 = Web3(
        Web3.HTTPProvider(
            "https://api.roninchain.com/rpc",
            request_kwargs={
                "headers": {
                    "content-type": "application/json",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
                }
            },
        )
    )
    """IF YOU HAVE YOUR OWN RPC URL, COMMENT OUT THE LINE ABOVE, UNCOMMENT THE LINE BELOW, AND ENTER IT ON THE LINE BELOW"""
    """w3 = Web3(Web3.HTTPProvider('https://ronin-testnet.skymavis.com/rpc'))"""
    abis = json.load(file)
    nonces = {}


def eth():
    """Get the eth contrant module"""
    eth_abi = abis["eth"]
    eth_address = Web3.toChecksumAddress("0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5")
    eth_contract = w3.eth.contract(address=eth_address, abi=eth_abi)
    return eth_contract


def marketplace():
    """Get the target marketplace"""
    marketplace_abi = abis["marketplace"]
    marketplace_address = Web3.toChecksumAddress(
        "0xfff9ce5f71ca6178d3beecedb61e7eff1602950e"
    )
    marketplace_contract = w3.eth.contract(
        address=marketplace_address, abi=marketplace_abi
    )
    return marketplace_contract


def send_txn(signed_txn, timeout=10):
    """Send transaction"""
    txn = signed_txn.hash  
    try:
        w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    except ValueError as e:
        print(e)

    tries = 0
    success = False
    while tries < 3:
        time.sleep(10)
        try:
            receipt = w3.eth.wait_for_transaction_receipt(txn, timeout)
            if receipt["status"] == 1:
                success = True
            break
        except (exceptions.TransactionNotFound, exceptions.TimeExhausted, ValueError):
            tries += 1
            print("Confirming transaction.Please wait...")
    if success:
        return True
    return False


def get_nonce(address):
    """Getting the nonce"""
    try:
        nonce = nonces[address]
        nonces[address] = nonce + 1
    except:
        nonce = w3.eth.get_transaction_count(Web3.toChecksumAddress(address))
        nonces[address] = nonce + 1
    return nonce


def send_txn_threads(txns, CONNECTIONS=100, TIMEOUT=10):
    """For transaction threads"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(send_txn, tx, TIMEOUT) for tx in txns)
        for future in concurrent.futures.as_completed(future_to_url):
            future.result()
