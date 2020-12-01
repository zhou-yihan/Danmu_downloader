# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:26:24 2020

@author: Yihan
"""

import requests, re
from bs4 import BeautifulSoup as BS
import pandas as pd
import time



# get danmu url in the past
def get_url_list(oid, start, end):
    url_list = []
    date_list = [i for i in pd.date_range(start, end).strftime('%Y-%m-%d')]
    for date in date_list:
        url = f"https://api.bilibili.com/x/v2/dm/history?type=1&oid={oid}&date={date}"
        url_list.append(url)
    return url_list

# get text from url
def open_url(url):
    headers = {"cookie": cookie,
    "origin": "https://www.bilibili.com",
    "referer": ma_url,
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
    response = requests.get(url, headers = headers)
    response.encoding = "utf-8"
    html = response.text
    return html

# change time from seconds to hour/min/sec
def format_time(seconds):
    seconds = eval(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:02%d" % (h, m, s)

# convert timestamp to date
def format_date(timestamp):
    return time.ctime(eval(timestamp))

# extract danmu_id
def get_danmu_id(html):
    try:
        danmu_id = re.findall(r'cid=(\d+)&', html)[0]
        return danmu_id
    except:
        return False


# read danmu via API
def get_danmu(url_list):
    danmu = open("C:/Users/Yihan/Desktop/ma.txt", 'w', encoding='utf8')
    for i in range(len(url_list)):
        url = url_list[i]     
        danmu_html = open_url(url)
        soup = BS(danmu_html, 'lxml')
        all_d = soup.select('d')
        for d in all_d:
            danmu_entry = d['p'].split(',')
            danmu_entry.append(d.get_text())
            danmu_entry[0] = format_time(danmu_entry[0])
            danmu_entry[4] = format_date(danmu_entry[4])
            #danmu_list.append(danmu_entry)
            #print(danmu_entry)
            danmu.write(','.join(danmu_entry)+"\n")
        print("Finished {}".format(url.split("=")[-1]))
    danmu.close()

'''
cookie = "_uuid=BBFEEF36-4ADE-F93C-F9D1-42575F060D8915609infoc; buvid3=E68CE157-DB13-4172-9BE2-8BD91855C7FC138379infoc; rpdid=0zbRF2HQUU|PXQ3XwR0|2T8|3w1Kar1M; blackside_state=1; LIVE_BUVID=AUTO1015988206194906; CURRENT_FNVAL=80; DedeUserID=404799053; DedeUserID__ckMd5=55d4bb2c6dc55509; SESSDATA=fad07c6b%2C1617581596%2C0f3d9*a1; bili_jct=d6cc0deafb794ef5c9dd439a9cedfe38; sid=j2htedln; bsource=search_google; finger=1295565314; CURRENT_QUALITY=64; PVID=1"
ma_url = "https://www.bilibili.com/video/BV1HJ411L7DP"
danmu_list = []
#set date interval
start = '1/1/2020'
end = '11/30/2020'
#get danmu ID
ma_html = open_url(ma_url)
danmu_id = get_danmu_id(ma_html)

#create urls in the past
url_list = get_url_list(danmu_id, start, end)
print(url_list)
#get danmu per each day
get_danmu(url_list)
'''

# 弹幕有重复，要去掉
danmu = pd.read_table("C:/Users/Yihan/Desktop/ma.txt", names = ["视频秒","模式", "字号", "颜色", "时间戳", "弹幕池", "ID", "历史弹幕", "弹幕内容"])

uniq_danmu = danmu.drop_duplicates()