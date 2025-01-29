# -*- coding: UTF-8 -*-
import requests
from http.server import BaseHTTPRequestHandler
import json
import re
headers = {
    "accept": "text/html",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "if-none-match": 'W/"ef80211272199b848c3cee5f9135b72d"',
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
}
def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
def getdata(name):
    gitpage = requests.get("https://github.com/" + name + "?action=show&controller=profiles&tab=contributions&user_id=" + name, headers=headers)
    # 写个正则匹配 datastr 中data-date 和 data-leve
    #  data-level="(\d+)"
    pattern = r'data-date="(\d{4}-\d{2}-\d{2})" id="contribution-day-component-\d-\d{1,2}" data-level="(\d+)"'
    matches = re.findall(pattern, gitpage.text)
    # 转成map {"2024-01-28":0,"2024-02-04":0,"2024-02-11":0}
    datemap = {item[0]:item[1] for item in matches}
    # 转成list ["2024-01-28","2024-02-04","2024-02-11"] 并且日期排序
    datadate = [item[0] for item in matches]
    datadate.sort()
    datalist = []
    datacount=0
    # 循环datadate 生成datalist
    for item in datadate:
        itemObj = {"date": item, "count": datemap[item]}
        datalist.append(itemObj)
        # datemap[item]} 是字符串
        datacount+=int(datemap[item])
    return {
        "total": datacount,
        "contributions": datalist
    }
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return

