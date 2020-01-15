import requests
import json
import tablib

url = 'https://www.xiaomiyoupin.com/api/gateway/detail'
payload = {
    'groupName': 'details',
    'groupParams': [[]],
    'methods': [],
    'version': '1.0.0',
    'debug': 'false',
    'channel': ''
}
headers = {
    
}
goods = []

for i in range(100000,120000) :
    payload['groupParams'] = [[str(i)]]
    r = requests.post(url, headers = headers, json=payload)
    r.encoding='utf-8'
    if r.status_code == 200 :
        res = r.json()
        data = res.get('data')
        gid =  data.get('gid')
        if gid is not None :
            name = data.get('goods').get('goodsInfo').get('name')
            item = []
            item.append(gid)
            item.append(name)
            goods.append(tuple(item))
            print(gid)
    else :
        print(r.status_code)

header = tuple(["gid","name"])
tbdata = tablib.Dataset(*goods,headers=header)
open('data.xls', 'wb').write(tbdata.xls)
