import time
from modules.sub_modules import db
from web3 import Web3
import modules.generate_access_token as generate_access_token
import modules.txn_utils as txn_utils
from modules.sub_modules import axie_functions
from cryptography.fernet import Fernet
import sys
from modules.sub_modules import save_key_ronin

sys.setrecursionlimit(10000)


MRKT_CONTRACT = Web3.toChecksumAddress("0xfff9ce5f71ca6178d3beecedb61e7eff1602950e")
WETH_CONTRACT = Web3.toChecksumAddress("0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5")
VALUE_TO_SPEND = (
    115792089237316195423570985008687907853269984665640564039457584007913129639935
)
CHAIN_ID = 2020
GAS = 481337




def get_list_of_keys():
    """Get the list of keys"""
    key_data = db.records("SELECT * FROM keys WHERE status =?", "active")
    db.commit

    """Variable Declarations"""
    if len(key_data) <= 0:
        print("No added ronin accounts yet")
        address = ""
        token = ""
        gas_price = ""
        eth_contract = ""
        mp_contract = ""
        pvt_key = ""
    else:
        """Decrypt the private key"""
        password, salt = save_key_ronin.read_KEK()
        decryption_key = save_key_ronin.get_decryption_key(password, salt)
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




def update_buy_count(axie_filter, filter_index):
    """Update buy_count on DB"""
    buy_count = db.field(
        "SELECT buy_count FROM snipe_list WHERE name = ?", axie_filter[filter_index][0]
    )
    db.execute(
        "UPDATE snipe_list SET buy_count = ? WHERE name = ?",
        int(buy_count) + int(1),
        axie_filter[filter_index][0],
    )
    db.commit()



def check_balance(balance, price):
    """Check if you still have a balance to buy another axie"""
    if balance <= price:
        print(
            f'You do not have enough ETH to buy anything. The lowest price you have set is {price / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH.\nTo continue, please complete the following steps: (1) deposit a sufficient amount of ETH, (2) restart the application (close and re-open), (3) click "Run Bot" for the desired filter.'
        )
        SystemExit

def run_loop(axie_filter, filter_index=0):
    """Running the loop to check if the axie is available"""
    loop_counter = 0
    num_to_buy=[]
    buy_count=[]

    for filter in axie_filter:
        num_to_buy.append(filter[3])
        buy_count.append(filter[5])

    try:
        while True:
            """If statement to see if the filter number to purchase is met If yes, skip"""
            if buy_count[filter_index]>=num_to_buy[filter_index]:
                filter_index += 1
                if filter_index > len(axie_filter)-1:
                    filter_index = 0
                continue
            else:
                if loop_counter == 1:
                    filter_index += 1

                    if filter_index > len(axie_filter)-1:
                        filter_index = 0
                    loop_counter = 0
                    continue
                
                """Variable declarations"""
                my_filter = eval(axie_filter[filter_index][2])
                filter_name = axie_filter[filter_index][0]
                price = Web3.toWei(axie_filter[filter_index][1], "ether")
                txns = []
                attempted_assets = []
                attempted_txns = {}
                balance = eth_contract.functions.balanceOf(address).call()

                """Check if you still have a balance to buy another axie"""
                if balance <= price:
                    print(
                        f'You do not have enough ETH to buy anything. The lowest price you have set is {price / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH.\nTo continue, please complete the following steps: (1) deposit a sufficient amount of ETH, (2) restart the application (close and re-open), (3) click "Run Bot" for the desired filter.'
                    )
                    break

                """Loop trough all the filters saved"""
                spend_amount = 0
                market = axie_functions.fetch_market(token, my_filter, filter_name)

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
                        num_to_buy[filter_index] -= 1
                        
                        if num_to_buy[filter_index] <= 0:
                                break
                
                """Verify Transactions"""
                if len(txns) > 0:
                    txn_utils.send_txn_threads(txns)
                    for tx in txns:
                        sent_txn = Web3.toHex(Web3.keccak(tx.rawTransaction))
                        receipt = txn_utils.w3.eth.get_transaction_receipt(sent_txn)
                        if not receipt.status == 1:
                            print(f"Failed to buy {attempted_txns[sent_txn]}.")
                        else:
                            print(
                                f"You successfully bought 1 {axie_filter[filter_index][0]} with {attempted_txns[sent_txn]} axie ID!"
                            )
                            update_buy_count(axie_filter, filter_index)
                            buy_count[filter_index]=buy_count[filter_index]+1

                    txns = []

                loop_counter += 1


    except Exception as e:
        print(f"Mainloop Error {e}")
        run_loop(axie_filter, filter_index)



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
    try:
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
    except: 
        pass

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
        print(f"You do not have enough ETH to buy anything.")


def print_list(axie_filter):
    """This is to print the current axies to run"""

    print("\nPending axie's to purchase...")
    print("***************************")
    print("Filtername | Purchase Limit")
    print("***************************")
    for filter_list in axie_filter:
        to_buy = filter_list[3] - filter_list[5]
        if to_buy < 1 :
            print(f"{filter_list[0]} | Rebuild to run again")
        else:
            print(f"{filter_list[0]} | {to_buy}")
    print("***************************\n")


def init():
    """Bot Initialization"""
    print("Initializing bot...")
    print(f"Your active ronin address is: {address}")
    check_available_ron()

    check_allowance()

    cheapest_filter = Web3.toWei(99999, "ether")
    can_afford = False
    balance = eth_contract.functions.balanceOf(address).call()

    axie_filter, axie_price = get_filterdata()

    check_can_afford(axie_price, balance, can_afford, cheapest_filter)
    
    print_list(axie_filter)
    print("Running Loop...")
    run_loop(axie_filter)

