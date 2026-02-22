import requests, json, os
from datetime import datetime
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REGION = "eu"

def get_access_token():
    url = "https://eu.battle.net/oauth/token"
    
    body = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=body, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    token_data = response.json()
    access_token = token_data['access_token']
    print("SUCCESS!")
    return access_token



def takeSnapshot(access_token):
    url = "https://eu.api.blizzard.com/data/wow/auctions/commodities"
    params = {
        'namespace': 'dynamic-eu',
        'locale': 'en_US'
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    print("Downloading")
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            serverTime = response.headers.get('Last-Modified')
            data = response.json()
            auctions = data['auctions']
            print(f"Downloaded {len(auctions)} auctions")
            return auctions, serverTime
    except Exception as e:
        print (F"ERROR {e}")

def save():
    myKey = get_access_token()
    folder = 'archive'
    os.makedirs(folder, exist_ok=True)
    if myKey:
        print("")
        snapshot, snapshotTime = takeSnapshot(myKey)
        datetimeObj = datetime.strptime(snapshotTime, "%a, %d %b %Y %H:%M:%S GMT")
        safeFilename = datetimeObj.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'{safeFilename}.json'
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=4)
            print("Saved as json")
        return snapshotTime
    

if __name__ == "__main__":
    save()
    pass
