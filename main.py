import os
import requests
import json
import lxml.html
import re

signIn = {'username': os.environ["USERNAME"], #学号
          'password': os.environ["PASSWORD"]} #登陆密码


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36',
}

conn = requests.Session()
signInResponse = conn.post(
    url="https://move.muc.edu.cn/uc/wap/login/check",
    headers=headers,
    data= signIn, 
    timeout=10
)

historyResponse = conn.get(
    url="https://move.muc.edu.cn/ncov/wap/default/index?from=history",
    headers=headers,
    data={'from': 'history'},
    timeout=10
)

historyResponse.encoding = "UTF-8"

html = lxml.html.fromstring(historyResponse.text)

JS = html.xpath('/html/body/script[@type="text/javascript"]')
JStr = JS[0].text

default = re.search('var def = {.*};',JStr).group()
oldInfo = re.search('oldInfo: {.*},',JStr).group()


Param = '"geo_api_info": { "type": "complete", "info": "SUCCESS", "status": 1, "position": {"O": 116.3270901582031, "P": 40.02177467243305, "lng": 116.3270901582031, "lat": 40.02177467243305}}'
        
           
newInfo = oldInfo
newInfo = newInfo.replace('oldInfo: {','{' + Param + ',').rstrip(',')

defaultStrip = default.replace('var def = ','').rstrip(';')
defdic = json.loads(defaultStrip)


dic = json.loads(newInfo)
dic['ismoved'] = '0'

for j in ["date","created","id","gwszdd","sfyqjzgc","jrsfqzys","jrsfqzfy"]:
    dic[j] = defdic[j]
    
dic['szgjcs'] = Param

saveResponse = conn.post(
    url="https://move.muc.edu.cn/ncov/wap/default/save",
    headers=headers,
    data = dic,
    timeout=10
)

saveJson = json.loads(saveResponse.text)
print(saveJson['m'])
