import requests
import datetime
import asyncio
import json
import numpy as np
from time import time

API_KEY = '8eb7c2bb-c304-470c-a821-b81085e45b55'

def tested(API_KEY):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {
        'start':'1',
        'limit':'10',
        'sort':'volume_24h',
        'sort_dir':'desc'
        }
    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
        }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url, params = parameters)
    
    return response

def freshness_test(response_json, i):
    current_timestamp = datetime.datetime.strptime(response_json['status']['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    last_update_timestamp = datetime.datetime.strptime(response_json['data'][i]['quote']['USD']['last_updated'], '%Y-%m-%dT%H:%M:%S.%fZ')
    timedelta = current_timestamp - last_update_timestamp
    assert timedelta.days == 0
    
def elapsed_test(response):
    elapsed_time = response.elapsed.total_seconds()
    assert elapsed_time < 0.5

def size_of_response_test(response):
    size = len(response.content)
    assert size < 10000

async def first_test(API_KEY):
    
    response = tested(API_KEY)
    response_json = json.loads(response.text)
    responses_elapsed.append(response.elapsed.total_seconds())

    size_of_response_test(response)

    elapsed_test(response)

    for i in range (10):
        freshness_test(response_json, i)
        
    await asyncio.sleep(0)

async def asynchronous(API_KEY):
    tasks = [asyncio.ensure_future(first_test(API_KEY)) for i in range (8)]
    await asyncio.wait(tasks)

def rps_test(full_elapsed_time):
    rps = 8 / full_elapsed_time
    assert rps > 5

def percentile_test(elapsed):
    np_elapsed = np.array(elapsed)
    latency = np.percentile(np_elapsed, 80)
    assert latency < 0.45

def second_test(API_KEY):
    start_timestamp = time()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asynchronous(API_KEY))
    
    end_timestamp = time()
    full_elapsed_time = end_timestamp - start_timestamp
    
    rps_test (full_elapsed_time)

if __name__ == '__main__':
    try:
        responses_elapsed = []
        second_test(API_KEY)
        percentile_test(responses_elapsed)
    except Exception as e:
        print ("Second test failed")
        print (e)


