import urllib.request
import json

def test_login():
    data = json.dumps({'phone': '13800000001', 'password': 'user123'}).encode()
    req = urllib.request.Request('http://localhost:8934/auth/login', data=data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print('会员登录成功:', result['user']['role'])
    return result['access_token']

def test_recommendations(token):
    req = urllib.request.Request('http://localhost:8934/match/recommendations', headers={'Authorization': 'Bearer ' + token})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print('推荐列表数量:', len(result))
    if result:
        print('=== Top 5 推荐 ===')
        for i, r in enumerate(result[:5]):
            print(f'{i+1}. {r["nickname"]} - {r["age"]}岁 - {r["city"]} - 匹配分:{r["match_score"]}')

def test_matchmaker_stats():
    data = json.dumps({'phone': 'matchmaker1', 'password': 'mm123'}).encode()
    req = urllib.request.Request('http://localhost:8934/auth/login', data=data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    token = result['access_token']
    print('红娘登录成功:', result['user']['role'])
    
    req2 = urllib.request.Request('http://localhost:8934/matchmaker/statistics', headers={'Authorization': 'Bearer ' + token})
    resp2 = urllib.request.urlopen(req2)
    stats = json.loads(resp2.read().decode())
    print('=== 平台统计 ===')
    print(f'会员总数: {stats["total_members"]}')
    print(f'男: {stats["male_count"]} / 女: {stats["female_count"]}')
    print(f'配对成功数: {stats["total_matches"]}')
    print(f'活动总数: {stats["total_activities"]}')

def test_activities(token):
    req = urllib.request.Request('http://localhost:8934/activities', headers={'Authorization': 'Bearer ' + token})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print('活动列表数量:', len(result))
    if result:
        for act in result:
            print(f'  - {act["name"]} ({act["status"]})')

if __name__ == '__main__':
    print('--- 测试会员功能 ---')
    token = test_login()
    test_recommendations(token)
    test_activities(token)
    
    print()
    print('--- 测试红娘功能 ---')
    test_matchmaker_stats()
    
    print()
    print('所有测试通过!')
