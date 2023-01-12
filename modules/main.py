import time
from . import db
from web3 import Web3
import modules.generate_access_token as generate_access_token
import modules.txn_utils as txn_utils
from . import axie_functions
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import tkinter.messagebox
import os
import sys



MRKT_CONTRACT = Web3.toChecksumAddress("0xfff9ce5f71ca6178d3beecedb61e7eff1602950e")
WETH_CONTRACT = Web3.toChecksumAddress("0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5")
VALUE_TO_SPEND = (
    115792089237316195423570985008687907853269984665640564039457584007913129639935
)
CHAIN_ID = 2020
GAS = 481337

gui_messages=[]

def resource_path(relative_path):
    """This function is for the path of additional files for tkinter"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_decryption_key(password, salt):
    """Get decryption key from the KEK using PBKDF2"""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=350000)
    decryption_key = base64.urlsafe_b64encode(kdf.derive(password))

    return decryption_key


def find_value(line):
    """Find value for password and salt"""
    line_value = line.rstrip("\n")
    value = line_value[line_value.index("=") + 1 :]
    return value



def read_KEK():
    """Read KEK from a file stored on disk"""
    with open("data\kek.txt", "r") as f:
        for line in f:
            if line.startswith("password"):
                password = bytes(find_value(line), "utf-8")
            if line.startswith("salt"):
                salt = bytes(find_value(line), "utf-8")
    return password, salt


def get_list_of_keys():
    """Get the list of keys"""
    key_data = db.records("SELECT * FROM keys WHERE status =?", "active")
    db.commit

    """Variable Declarations"""
    if len(key_data) <= 0:
        print("No added ronin accounts yet")
        address=""
        token=""
        gas_price=""
        eth_contract=""
        mp_contract=""
        pvt_key=""
    else:
        """Decrypt the private key"""
        password, salt = read_KEK()
        decryption_key = get_decryption_key(password, salt)
        f = Fernet(decryption_key)

        pvt_key_bytes = f.decrypt(key_data[0][0])
        pvt_key = pvt_key_bytes.decode("utf-8")
        ron_add = key_data[0][1]
        address = Web3.toChecksumAddress(ron_add.replace("ronin:", "0x"))
        token = generate_access_token.generate_access_token(pvt_key, address)
        gas_price = key_data[0][2]
        eth_contract = txn_utils.eth()
        mp_contract = txn_utils.marketplace()

    return address, token, gas_price, eth_contract, mp_contract, pvt_key


address, token, gas_price, eth_contract, mp_contract, pvt_key = get_list_of_keys()


def approve():
    """Approve ETH to spend"""
    try_send_txn = eth_contract.functions.approve(
        Web3.toChecksumAddress(MRKT_CONTRACT),
        VALUE_TO_SPEND,
    ).buildTransaction(
        {
            "chainId": CHAIN_ID,
            "gas": GAS,
            "gasPrice": Web3.toWei(1, "gwei"),
            "nonce": txn_utils.get_nonce(address),
        }
    )
    signed_txn = txn_utils.w3.eth.account.sign_transaction(
        try_send_txn, private_key=pvt_key
    )
    sent_txn = Web3.toHex(Web3.keccak(signed_txn.rawTransaction))
    txn_utils.send_txn(signed_txn)
    return sent_txn


def buy_asset(asset):
    """This function is used to purchase the axie"""
    order = asset["order"]
    market_txn = mp_contract.functions.interactWith(
        "ORDER_EXCHANGE",
        mp_contract.encodeABI(
            fn_name="settleOrder",
            args=[
                0,
                int(order["currentPrice"]),
                Web3.toChecksumAddress(address),
                order["signature"],
                [
                    Web3.toChecksumAddress(order["maker"]),
                    1,
                    [
                        [
                            1,
                            Web3.toChecksumAddress(order["assets"][0]["address"]),
                            int(order["assets"][0]["id"]),
                            int(order["assets"][0]["quantity"]),
                        ]
                    ],
                    int(order["expiredAt"]),
                    Web3.toChecksumAddress(WETH_CONTRACT),
                    int(order["startedAt"]),
                    int(order["basePrice"]),
                    int(order["endedAt"]),
                    int(order["endedPrice"]),
                    0,
                    int(order["nonce"]),
                    425,
                ],
            ],
        ),
    ).buildTransaction(
        {
            "chainId": CHAIN_ID,
            "gas": GAS,
            "gasPrice": Web3.toWei(int(gas_price), "gwei"),
            "nonce": txn_utils.get_nonce(address),
        }
    )

    print(market_txn)
    signed_txn = txn_utils.w3.eth.account.sign_transaction(
        market_txn, private_key=pvt_key
    )
    return signed_txn


def check_filter_limit(num_to_buy, bought_axie, filter_name):
    """Check if you reached the filter limit"""
    if num_to_buy >= bought_axie:
        print("The filter buy limit has been reached.")
        tkinter.messagebox.showinfo(
            "Bloodmoon Sniper Bot",
            f"Filter limit reached for {filter_name}.",
        )
        return True
    else:
        return False

def update_buy_count(axie_filter,filter_index):
    """Update buy_count on DB"""
    buy_count = db.field("SELECT buy_count FROM snipe_list WHERE name = ?", axie_filter[filter_index][0])
    db.execute("UPDATE snipe_list SET buy_count = ? WHERE name = ?", int(buy_count) + int(1), axie_filter[filter_index][0])
    db.commit()

    

def verify_transactions(txns, attempted_txns,axie_filter,filter_index):
    """Verify if the transaction succeded"""
    if len(txns) > 0:
        txn_utils.send_txn_threads(txns)
        for tx in txns:
            sent_txn = Web3.toHex(Web3.keccak(tx.rawTransaction))
            receipt = txn_utils.w3.eth.get_transaction_receipt(sent_txn)
            if not receipt.status == 1:
                num_to_buy += 1
                print(f"Failed to buy {attempted_txns[sent_txn]}.")
            else:
                print(f"You successfully bought 1 {axie_filter[filter_index][0]} with {attempted_txns[sent_txn]} axie ID!")
                update_buy_count(axie_filter,filter_index)

        txns = []

    return txns


def check_num_to_buy(num_to_buy, num_asset, axie_filter, filter_index):
    """Check if you still need to buy anoter axie with this filter"""
    if num_to_buy <= 0:
        print(f"Bought {num_asset} axie/s. This is the limit.")
        return run_loop(axie_filter, filter_index + 1)


def check_balance(balance, price):
    """Check if you still have a balance to buy another axie"""
    if balance <= price:
        print(
            f'You do not have enough ETH to buy anything. The lowest price you have set is {price / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH.\nTo continue, please complete the following steps: (1) deposit a sufficient amount of ETH, (2) restart the application (close and re-open), (3) click "Run Bot" for the desired filter.'
        )
        raise SystemExit


def run_loop(axie_filter, filter_index=0):
    """Running the loop to check if the axie is available"""

    """If statement to see if the filter number to purchase is met If yes, skip"""
    if check_filter_limit(
        axie_filter[filter_index][5],
        axie_filter[filter_index][3],
        axie_filter[filter_index][0],
    ):
        run_loop(axie_filter, filter_index + 1)
    else:
        """Variable declarations"""
        my_filter = eval(axie_filter[filter_index][2])
        filter_name = axie_filter[filter_index][0]
        num_asset = axie_filter[filter_index][3]
        price = Web3.toWei(axie_filter[filter_index][1], "ether")
        txns = []
        attempted_assets = []
        attempted_txns = {}
        count = 0
        num_to_buy = num_asset
        balance = eth_contract.functions.balanceOf(address).call()
        """Loop trough all the filters saved"""
        try:
            while True:
                spend_amount = 0

                market = axie_functions.fetch_market(token, my_filter,filter_name)

                for asset in market["data"]["axies"]["results"]:
                    if "id" in asset and asset["id"] in attempted_assets:
                        continue
                    elif "tokenId" in asset and asset["tokenId"] in attempted_assets:
                        continue
                    if price >= int(asset["order"]["currentPrice"]):
                        if (
                            int(asset["order"]["endedPrice"]) == 0
                            and int(asset["order"]["endedAt"]) == 0
                        ):
                            price_change = 0
                        else:
                            price_change = (
                                int(asset["order"]["endedPrice"])
                                - int(asset["order"]["basePrice"])
                            ) / int(asset["order"]["duration"])
                        # this is to check if they are doing a sale from 0 -> 10000 over 1 day in attempt to fool bots.
                        # worst case, a tx takes 10 seconds from when it was pulled from marketplace to when it goes through
                        # i doubt it will ever take 10s, but would rather be safe.
                        # feel free to change the 10 to something less if you want to (at your own risk)
                        if (
                            int(asset["order"]["currentPrice"]) + (price_change * 10)
                            > price
                        ):
                            if "id" in asset:
                                print(
                                    f"not buying {asset['id']}, someone is doing something funky."
                                )
                            else:
                                print(
                                    f"not buying {asset['tokenId']}, someone is doing something funky."
                                )
                            continue

                        spend_amount += int(asset["order"]["currentPrice"])
                        if spend_amount > balance:
                            break
                        tx = buy_asset(asset)
                        txns.append(tx)

                        if "id" in asset:
                            print(f"Attempting to buy axie #{asset['id']}.")
                            attempted_txns[
                                Web3.toHex(Web3.keccak(tx.rawTransaction))
                            ] = asset["id"]
                            attempted_assets.append(asset["id"])

                        else:
                            print(f"Attempting to buy axie #{asset['tokenId']}.")
                            attempted_txns[
                                Web3.toHex(Web3.keccak(tx.rawTransaction))
                            ] = asset["tokenId"]
                            attempted_assets.append(asset["tokenId"])
                        num_to_buy -= 1
                        if num_to_buy <= 0:
                            break

                """Verify Transactions"""
                txns = verify_transactions(txns, attempted_txns,axie_filter,filter_index)

                """Check if you reached the limit to buy"""
                check_num_to_buy(num_to_buy, num_asset, axie_filter, filter_index)

                """Check if you still have balance to buy the axie"""
                balance = eth_contract.functions.balanceOf(address).call()
                check_balance(balance, price)

                count += 1

                if count % 120 == 0:
                    print("Still searching marketplace.")
                time.sleep(1)
        except:
            pass


def check_available_ron():
    """Check acailable RON balance"""
    print("Checking RON balance...")
    ron_bal = txn_utils.w3.eth.get_balance(address)
    if ron_bal < (481337 * Web3.toWei(int(gas_price), "gwei")):
        print(
            "You do not have enough RON for the entered gas price. Please lower gas price or add more RON."
        )
        raise SystemExit


def check_allowance():
    """Check allowance. If 0 continue to approve"""
    allowance = eth_contract.functions.allowance(address, MRKT_CONTRACT).call()

    if allowance == 0:
        print("Approving ETH to spend...")
        sent_txn = approve()
        allowance = eth_contract.functions.allowance(address, MRKT_CONTRACT).call()

        if allowance == 0:
            print("Something went wrong, approval didnt work. Exiting.")
            raise SystemExit
        else:
            print(f"Approved at txn: {sent_txn}")


def get_filterdata():
    """Get filter data from DB"""
    axie_filter = db.records("SELECT * FROM snipe_list")
    db.commit
    axie_price = Web3.toWei(axie_filter[0][1], "ether")
    return axie_filter, axie_price


def check_can_afford(axie_price, balance, can_afford, cheapest_filter):
    """Check if the user can afford the current filter"""
    if axie_price < balance:
        can_afford = True

    if axie_price < cheapest_filter:
        cheapest_filter = axie_price

    if not can_afford:
        print(
            f"You do not have enough ETH to buy anything."
        )
        tkinter.messagebox.showinfo(
            "Bloodmoon Sniper",
            f"You do not have enough ETH to buy anything.",
        )

def print_list(axie_filter):
    """This is to print the current axies to run"""

    print("\nPending axie's to purchase...")
    print("***************************")
    print("Filtername | Purchase Limit")
    print("***************************")
    for filter_list in axie_filter:
        to_buy = filter_list[3]-filter_list[5]
        if to_buy == 0 :
           print(f"{filter_list[0]} | Rebuild to run again")
        else:
            print(f"{filter_list[0]} | {to_buy}")
    print("***************************\n")

def init():
    """Bot Initialization"""
    print("Initializing bot...")
    check_available_ron()

    check_allowance()

    cheapest_filter = Web3.toWei(99999, "ether")
    can_afford = False
    balance = eth_contract.functions.balanceOf(address).call()

    axie_filter, axie_price = get_filterdata()
    print_list(axie_filter)

    check_can_afford(axie_price, balance, can_afford, cheapest_filter)
    
    try:
        run_loop(axie_filter)
    except Exception as e:
        print(e)
