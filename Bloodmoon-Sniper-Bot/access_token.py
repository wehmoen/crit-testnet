import json
import requests
from eth_account.messages import encode_defunct
from web3 import Web3


def signRoninMessage(message, key, attempts2=0):
    # for singning ronin message
    try:
        mes = encode_defunct(text=message)
        ronweb3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc'))
        # ronweb3 = Web3(Web3.HTTPProvider('https://ronin-testnet.skymavis.com/rpc'))
        sig = ronweb3.eth.account.sign_message(mes, private_key=key)
        signature = sig['signature'].hex()
        return signature
    except Exception as e:
        if attempts2 > 3:
            print("Could not Sign Message. Are the servers having issues?")
            print(e)
            return None
        else:
            return signRoninMessage(message, key, attempts2 + 1)


def generate_access_token(key, address, attempts=0):
    # for generating access token
    def getRandomMessage(attempts2=0):
        try:
            url = "https://graphql-gateway.axieinfinity.com/graphql"

            payload = '{"query":"mutation CreateRandomMessage{createRandomMessage}","variables":{}}'
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            return json_data['data']['createRandomMessage']
        except Exception as e:
            if attempts2 > 3:
                print("Could not generate AccessToken Random Message. Are the servers having issues?")
                print(e)
                return None
            else:
                return getRandomMessage(attempts2 + 1)


    def signRoninMessage(message, key, attempts2=0):
        try:
            mes = encode_defunct(text=message)
            ronweb3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc'))
            # ronweb3 = Web3(Web3.HTTPProvider('https://ronin-testnet.skymavis.com/rpc'))
            sig = ronweb3.eth.account.sign_message(mes, private_key=key)
            signature = sig['signature'].hex()
            return signature
        except Exception as e:
            if attempts2 > 3:
                print("Could not Sign Message. Are the servers having issues?")
                print(e)
                return None
            else:
                return signRoninMessage(message, key, attempts2 + 1)

    def CreateAccessToken(message, signature, address, attempts2=0):
        try:
            url = "https://graphql-gateway.axieinfinity.com/graphql"
            payload = '{"query":"mutation CreateAccessTokenWithSignature($input:SignatureInput!){createAccessTokenWithSignature(input:$input){newAccount,result,accessToken,__typename}}","variables":{"input":{"mainnet":"ronin","owner":"' + address + '","message":"' + message + '","signature":"' + signature + '"}}}'
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            json_data = json.loads(response.text)
            return json_data['data']['createAccessTokenWithSignature']['accessToken']
        except Exception as e:
            if attempts2 > 3:
                print("Could not Create Access Token. Are the servers having issues?")
                print(e)
                return None
            else:
                return CreateAccessToken(message, signature, address, attempts2 + 1)

    try:
        myResponse = getRandomMessage()
        mySignature = signRoninMessage(myResponse, key)
        token = CreateAccessToken(repr(myResponse).replace("\'", ""), mySignature, address)
        return token
    except Exception as e:
        if attempts > 3:
            print(e)
            print("Unable To generate Access Token. This is gernerally an internet issue or a server issue.")
            return None
        else:
            return generate_access_token(key, address, attempts + 1)


# pvtkey="0x759af3892a7222ac125161b990a8f8f177332297b5b493c515c5a59348ec5e55"
# roninadd="ronin:1b8f7ff261ae5a10ab6918a86a2e508e7191aaec"
# print(generate_access_token(pvtkey,roninadd))
