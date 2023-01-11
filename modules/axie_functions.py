import requests
import json
import traceback
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import datetime
import bloodmoon_main

def fetch_market(access_token, my_filter,filter_name,attempts=0):
    """Fetch listing from marketplace with the desired filter"""
    url = "https://graphql-gateway.axieinfinity.com/graphql"
    
    try:
        del my_filter['specialCollection']
        print(f"Searching for {filter_name}...")
    except:  
        print(f"\nSearching for {filter_name}...")
        print("Non Special Collection")
        print("current time:-",datetime.datetime.now())

    payload = {
        "query": "query GetAxieBriefList($auctionType:AuctionType,$criteria:AxieSearchCriteria,$from:Int,$sort:SortBy,$size:Int,$owner:String){axies(auctionType:$auctionType,criteria:$criteria,from:$from,sort:$sort,size:$size,owner:$owner,){total,results{id,order{...on Order{id,maker,kind,assets{...on Asset{erc,address,id,quantity,orderId}}expiredAt,paymentToken,startedAt,basePrice,endedAt,endedPrice,expectedState,nonce,marketFeePercentage,signature,hash,duration,timeLeft,currentPrice,suggestedPrice,currentPriceUsd}}}}}",
        "variables": {
            "from": 0,
            "size": 100,
            "sort": "PriceAsc",
            "auctionType": "Sale",
            "owner": None,
            "criteria": my_filter,
        },
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    }
    try:
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload)
        )
    except:
        if attempts >= 3:
            print("fetchAxieMarket request")
            print("something is wrong. exiting the program.")
            print(traceback.format_exc())
            raise SystemExit
        return fetch_market(access_token, my_filter, attempts + 1)
    try:
        temp = json.loads(response.text)["data"]["axies"]["total"]
        if temp >= 0:
            return json.loads(response.text)
    except:
        if attempts >= 3:
            print("Fetch Axie Market...")
            print("something is wrong. exiting the program.")
            print("filter:\t" + json.dumps(my_filter))
            print("response:\t" + response.text)
            print(traceback.format_exc())
            raise SystemExit
        return fetch_market(access_token, my_filter, attempts + 1)


def checkFilter(access_token, my_filter, attempts=0):
    """Check if the filter exist"""
    url = "https://graphql-gateway.axieinfinity.com/graphql"

    payload = {
        "query": "query GetAxieBriefList($auctionType:AuctionType,$criteria:AxieSearchCriteria,$from:Int,$sort:SortBy,$size:Int,$owner:String){axies(auctionType:$auctionType,criteria:$criteria,from:$from,sort:$sort,size:$size,owner:$owner){total}}",
        "variables": {
            "from": 0,
            "size": 0,
            "sort": "PriceAsc",
            "auctionType": "All",
            "owner": None,
            "criteria": my_filter,
        },
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    }

    # this block of code is to prevent from timeout on the request
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.request(
            "POST", url, headers=headers, data=json.dumps(payload)
        )
    except:
        if attempts >= 3:
            print("checkAxieFilter request")
            print("something is wrong. exiting the program.")
            print(traceback.format_exc())
            raise SystemExit
        return checkFilter(access_token, my_filter, attempts + 1)
    try:
        return json.loads(response.text)["data"]["axies"]["total"]
    except:
        if attempts >= 3:
            print("checkAxieFilter")
            print("something is wrong. exiting the program.")
            print("filter:\t" + json.dumps(my_filter))
            print("response:\t" + response.text)
            print(traceback.format_exc())
            raise SystemExit
        return checkFilter(access_token, my_filter, attempts + 1)
