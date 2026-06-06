import urllib.request
import json
import urllib.error

def test_login_and_recommend():
    data = json.dumps({'phone': '13800000001', 'password': 'user123'}).encode()
    req = urllib.request.Request('http://localhost:8934/auth/login', data=data, headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read().decode())
        print('登录成功:', result['user']['phone'])
        token = result['access_token']
        
        req2 = urllib.request.Request('http://localhost:8934/match/recommendations', headers={'Authorization': 'Bearer ' + token})
        resp2 = urllib.request.urlopen(req2)
        result2 = json.loads(resp2.read().decode())
        print('推荐数量:', len(result2))
        if result2:
            print('Top 5:')
            for r in result2[:5]:
                print(f"  {r['nickname']} - {r['age']}岁 - {r['city']} - 匹配分:{r['match_score']}")
    except urllib.error.HTTPError as e:
        print('错误:', e.code, e.read().decode())

if __name__ == '__main__':
    test_login_and_recommend()
