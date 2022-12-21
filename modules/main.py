import time
from data import db
import modules.save_key_ronin as save_key_ronin
from web3 import Web3
import modules.generate_access_token as generate_access_token
import modules.txn_utils as txn_utils
from asset_func import axie_functions
from cryptography.fernet import Fernet
import modules.create_filter as create_filter
import tkinter.messagebox


"""Get the list of keys"""
key_data = db.records("SELECT * FROM keys WHERE status =?", "active")
db.commit

if len(key_data) <= 0:
    print("No data")
else:
    """Decrypt the private key"""
    fernet_key = key_data[0][3]
    f = Fernet(fernet_key)

    pvt_key_bytes = f.decrypt(key_data[0][0])

    pvt_key = pvt_key_bytes.decode("utf-8")
    ron_add = key_data[0][1]

    address = Web3.toChecksumAddress(ron_add.replace("ronin:", "0x"))
    token = generate_access_token.generate_access_token(pvt_key, address)
    gas_price = 1
eth_contract = txn_utils.eth()
mp_contract = txn_utils.marketplace()


def get_key_list():
    if True:
        """Get the list of keys"""
        key_data = db.records("SELECT * FROM keys WHERE status =?", "active")
        db.commit

        if len(key_data) <= 0:
            print("No data")
        else:
            """Decrypt the private key"""
            fernet_key = key_data[0][3]
            f = Fernet(fernet_key)

            pvt_key_bytes = f.decrypt(key_data[0][0])

            pvt_key = pvt_key_bytes.decode("utf-8")
            ron_add = key_data[0][1]

            address = Web3.toChecksumAddress(ron_add.replace("ronin:", "0x"))
            token = generate_access_token.generate_access_token(pvt_key, address)
            gas_price = 1
        eth_contract = txn_utils.eth()
        mp_contract = txn_utils.marketplace()


def approve():
    """Approve ETH to spend"""
    try_send_txn = eth_contract.functions.approve(
        Web3.toChecksumAddress("0xfff9ce5f71ca6178d3beecedb61e7eff1602950e"),
        115792089237316195423570985008687907853269984665640564039457584007913129639935,
    ).buildTransaction(
        {
            "chainId": 2020,
            "gas": 481337,
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
                Web3.toChecksumAddress("0xa8Da6b8948D011f063aF3aA8B6bEb417f75d1194"),
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
                    Web3.toChecksumAddress(
                        "0xc99a6A985eD2Cac1ef41640596C5A5f9F4E19Ef5"
                    ),
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
            "chainId": 2020,
            "gas": 481337,
            "gasPrice": Web3.toWei(int(gas_price), "gwei"),
            "nonce": txn_utils.get_nonce(address),
        }
    )
    signed_txn = txn_utils.w3.eth.account.sign_transaction(
        market_txn, private_key=pvt_key
    )
    return signed_txn


def run_loop(axie_filter, filter_index=0):
    """Running the loop to check if the axie is available"""
    """If statement to see if the filter number to purchase is met If yes, skip"""
    if axie_filter[filter_index][5] >= axie_filter[filter_index][3]:
        print("The filter buy limit has been reached.")
        tkinter.messagebox.showinfo(
            "Bloodmoon Sniper Bot",
            f"Filter limit reached for {axie_filter[filter_index][0]}.",
        )
        run_loop(axie_filter, filter_index + 1)
    else:
        my_filter = eval(axie_filter[filter_index][2])
        num_asset = axie_filter[filter_index][3]
        price = Web3.toWei(axie_filter[filter_index][1], "ether")
        txns = []
        attempted_assets = []
        attempted_txns = {}
        count = 0
        num_to_buy = num_asset
        balance = eth_contract.functions.balanceOf(address).call()
        while True:
            spend_amount = 0

            market = axie_functions.fetch_market(token, my_filter)

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
                        print(f"Attempting to buy asset #{asset['id']}.")
                        attempted_txns[
                            Web3.toHex(Web3.keccak(tx.rawTransaction))
                        ] = asset["id"]
                        attempted_assets.append(asset["id"])

                    else:
                        print(f"Attempting to buy asset #{asset['tokenId']}.")
                        attempted_txns[
                            Web3.toHex(Web3.keccak(tx.rawTransaction))
                        ] = asset["tokenId"]
                        attempted_assets.append(asset["tokenId"])
                    num_to_buy -= 1
                    if num_to_buy <= 0:
                        break
            print(txns)
            if len(txns) > 0:
                txn_utils.send_txn_threads(txns)
                for tx in txns:
                    sent_txn = Web3.toHex(Web3.keccak(tx.rawTransaction))
                    receipt = txn_utils.w3.eth.get_transaction_receipt(sent_txn)
                    if not receipt.status == 1:
                        num_to_buy += 1
                        print(f"Buying asset {attempted_txns[sent_txn]} failed.")
                    else:
                        print(f"Buying asset {attempted_txns[sent_txn]} succeded.")

                txns = []

            if num_to_buy <= 0:
                print(f"Bought {num_asset} assets. This is the limit. Exiting.")
                tkinter.messagebox.showinfo(
                    "Bloodmoon Sniper Bot",
                    f"Bought {num_asset} assets. This is the limit. Returning to main menu",
                )
                return run_loop(axie_filter, filter_index + 1)

            balance = eth_contract.functions.balanceOf(address).call()

            if balance <= price:
                print(
                    f"You do not have enough ETH to buy anything. Current price you have set is {price / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting."
                )
                tkinter.messagebox.showinfo(
                    "Bloodmoon Sniper Bot",
                    f"You do not have enough ETH to buy anything. Current price you have set is {price / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting.",
                )
                raise SystemExit
            count += 1

            if count % 120 == 0:
                print("Still searching marketplace.")
            time.sleep(1)


def init():
    """Bot Initialization"""
    ron_bal = txn_utils.w3.eth.get_balance(address)
    if ron_bal < (481337 * Web3.toWei(int(gas_price), "gwei")):
        print(
            "You do not have enough RON for the entered gas price. Please lower gas price or add more RON."
        )
        raise SystemExit
    allowance = eth_contract.functions.allowance(
        address, "0xffF9Ce5f71ca6178D3BEEcEDB61e7Eff1602950E"
    ).call()
    if allowance == 0:
        print("We need to approve eth for spending on the marketplace. Approving...")
        sent_txn = approve()
        allowance = eth_contract.functions.allowance(
            address, "0xffF9Ce5f71ca6178D3BEEcEDB61e7Eff1602950E"
        ).call()
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

    axie_price = Web3.toWei(axie_filter[0][1], "ether")

    if axie_price < balance:
        can_afford = True

    if axie_price < cheapest_filter:
        cheapest_filter = axie_price

    if not can_afford:
        print(
            f"You do not have enough ETH to buy anything. Current cheapest filter price you have set is {cheapest_filter / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH. Exiting."
        )
        tkinter.messagebox.showinfo(
            "Bloodmoon Sniper",
            f"You do not have enough ETH to buy anything. Current cheapest filter price you have set is {cheapest_filter / (10 ** 18)} ETH and you only have {balance / (10 ** 18)} ETH.",
        )

    print("Searching for Axies...")
    run_loop(axie_filter)


