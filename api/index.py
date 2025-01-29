# -*- coding: UTF-8 -*-
import requests
from http.server import BaseHTTPRequestHandler
import json
# from bs4 import BeautifulSoup
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
    # data = BeautifulSoup(gitpage.text, 'html.parser')  
    return {
        "data":gitpage.text
    }
    # dataEle = data.find_all('td', class_='ContributionCalendar-day', attrs={'data-date': True})
    # datadate = [item.attrs['data-date'] for item in dataEle]
    # datacount = [int(item.attrs['data-level']) for item in dataEle]
    # contributions = sum(datacount)
    # datalist = []

    # for index, item in enumerate(datadate):
    #     itemlist = {"date": item, "count": datacount[index]}
    #     datalist.append(itemlist)
    # datalistsplit = list_split(datalist, 7)
    # returndata = {
    #     "total": contributions,
    #     "contributions": datalistsplit
    # }
    # return returndata
# fetch("https://github.com/cxvh?action=show&controller=profiles&tab=contributions&user_id=cxvh", {
#   "headers": {
#     "accept": "text/html",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "if-none-match": "W/\"ef80211272199b848c3cee5f9135b72d\"",
#     "priority": "u=1, i",
#     "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"macOS\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-requested-with": "XMLHttpRequest"
#   },
#   "referrer": "https://github.com/cxvh",
#   "referrerPolicy": "strict-origin-when-cross-origin",
#   "body": null,
#   "method": "GET",
#   "mode": "cors",
#   "credentials": "include"
# }).then(res=>res.text())
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

