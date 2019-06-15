import requests
import datetime
import json

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

def first_test(API_KEY):
    response = tested(API_KEY)
    response_json = json.loads(response.text)
    
    size_of_response_test(response)
    
    elapsed_test(response)
    
    for i in range (10):
        freshness_test(response_json, i)
        
    return response_json

if __name__ == '__main__':
    try:
        first_test(API_KEY)
    except Exception as e:
        print ("First test failed")
        print (e)
