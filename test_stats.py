import urllib.request
import json

def login(phone, password):
    data = json.dumps({'phone': phone, 'password': password}).encode()
    req = urllib.request.Request('http://localhost:8934/auth/login', data=data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    return result['access_token']

def get_stats(token):
    req = urllib.request.Request('http://localhost:8934/matchmaker/statistics', headers={'Authorization': 'Bearer ' + token})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())

if __name__ == '__main__':
    token = login('matchmaker1', 'mm123')
    stats = get_stats(token)
    print('=== 平台统计 ===')
    for k, v in stats.items():
        print(f'{k}: {v}')
