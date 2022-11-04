import json
import time
import traceback
import requests
from utils import db
import key_ronin
from web3 import Web3
import access_token
import txn_utils
import asset_filter
from asset_func import axie_functions
from cryptography.fernet import Fernet

if True:
    key_data = db.records("SELECT * FROM keys")
    db.commit

    
    if len(key_data)<=0:
        key_ronin.add_key_address()
    else:
        # Decrypt the private key
        fernet_key = key_data[0][3]
        f = Fernet(fernet_key)

        pvt_key_bytes = f.decrypt(key_data[0][0])
        
        pvt_key = pvt_key_bytes.decode('utf-8')
        ron_add = key_data[0][1]

        address = Web3.toChecksumAddress(ron_add.replace("ronin:", "0x"))
        token= access_token.generate_access_token(pvt_key,address)
        gas_price = key_data[0][2]
        
    eth_contract = txn_utils.eth()
    mp_contract = txn_utils.marketplace()
    
    

    def approve():
        send_txn = eth_contract.functions.approve(
            Web3.toChecksumAddress('0xfff9ce5f71ca6178d3beecedb61e7eff1602950e'),
            115792089237316195423570985008687907853269984665640564039457584007913129639935
        ).buildTransaction({
            'chainId': 2020,
            'gas': 481337,
            'gasPrice': Web3.toWei(1, 'gwei'),
            'nonce': txn_utils.getNonce(address)
        })
        signed_txn = txn_utils.w3.eth.account.sign_transaction(send_txn, private_key=pvt_key)
        sentTx = Web3.toHex(Web3.keccak(signed_txn.rawTransaction))
        txn_utils.sendTx(signed_txn)
        return sentTx

    # print(token)




def init():
    ron_bal = txn_utils.w3.eth.get_balance(address)
    if ron_bal<(481337 * Web3.toWei(int(gas_price), 'gwei')):
        print("You do not have enough RON for the entered gas price. Please lower gas price or add more RON.")
        raise SystemExit
    allowance = eth_contract.functions.allowance(address, "0xffF9Ce5f71ca6178D3BEEcEDB61e7Eff1602950E").call()
    if allowance== 0:
        print("We need to approve eth for spending on the marketplace. Approving...")
        sent_txn = approve()
        allowance = eth_contract.functions.allowance(address, "0xffF9Ce5f71ca6178D3BEEcEDB61e7Eff1602950E").call()
        if allowance == 0:
            print("Something went wrong, approval didnt work. Exiting.")
            raise SystemExit
        else:
            print(f"Approved at tx: {sent_txn}")

    cheapest_filter = Web3.toWei(99999, "ether")
    can_afford = False
    balance = eth_contract.functions.balanceOf(address).call()
    
    axie_filter = db.records("SELECT * FROM snipe_list")
    db.commit
    axie_price =Web3.toWei(axie_filter[0][1],'ether')
   

    if axie_price< balance:
        can_afford = True
    
    if axie_price < cheapest_filter:
        cheapest_filter = axie_price
    
    if not can_afford:
        print(f"You do not have enough ETH to buy anything. Current cheapest filter price you have set is {cheapest_filter / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting.")
        raise SystemExit

    print("Checking marketplace...")

    for x in range(len(axie_filter)):
        try:
            ax_price = Web3.toWei(axie_filter[x][1],'ether')
            market=axie_functions.fetchMarket(token, axie_filter[x][2])
        except:
            print("Something went wrong.")

        cheapest = Web3.toWei(99999, "ether")
        count = 0

        for asset in market['data']['axies']['results']:
            if ax_price >= int(asset['order']['currentPrice']):
                count += 1
            if int(asset['order']['currentPrice'])<cheapest:
                cheapest = int(asset['order']['currentPrice'])
            if count > 0:
                print(f"There are at least {count} assets that are less than the price you have set in the filter {axie_filter[x][0]}.")
                print(f"Current cheapest asset is {cheapest / (10 ** 18)} ETH and your buy price is {ax_price / (10 ** 18)} ETH.")
                user_input = input("Would you like to remove this filter? Saying no, will send you back to main menu where you can edit it. (Y/N)\n").lower()
                if not user_input == "y":
                    print("You have chosen not to continue. Choose option 2 from the main menu to edit your filter.")
                    return asset_filter.main_menu()
                else:
                    print("Deleting Filter"+axie_filter[x][2])
                    db.execute(f"DELETE from snipe_list WHERE name = {axie_filter[x][2]}")
    time.sleep(1)
    print("Starting Sniper Bot")

init()