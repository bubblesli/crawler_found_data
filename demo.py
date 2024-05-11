import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/your_chrome_version Safari/537.36',
    }
fund_url = "https://fundf10.eastmoney.com/jjjz_002583.html"
chrome_exe_path = r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
#创建浏览器实例
chromedrives = 'D:/python/Python37/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe'
options = webdriver.ChromeOptions()
options.binary_location = chrome_exe_path
options.add_argument('--disable-dev-shm-usage')  # 禁用共享内存
options.add_argument('--no-sandbox')  # 忽略沙箱
options.add_argument('--remote-debugging-port=9222')  # 设置调试端口
service = Service(chromedrives)
driver = webdriver.Chrome(service=service, options=options)
#driver = webdriver.Chrome()
#访问网页
driver.get(fund_url)
time.sleep(5)
#response = requests.get(fund_url, headers=headers)
#获取包括动态加载内容的页面源码
html_content = driver.page_source
#关闭浏览器
driver.quit()
soup = BeautifulSoup(html_content, 'lxml')
result = soup.find_all(class_='w782 comm lsjz')
grouped_data = []
curren_group = []
for td in result:
    if 'class' in td.attrs and 'red unbold' in td['class']:
        if curren_group:
            grouped_data.append(curren_group)
            curren_group = []
    else:
        curren_group.append(td.text)
if curren_group:
    grouped_data.append(curren_group)

result_data = []
for sublist in grouped_data:
    lines = sublist.split('\n')
    for i in lines:
        if i == '':
            continue
        elif i == '净值日期':
            continue
        elif i == '单位净值':
            continue
        elif i == '累计净值':
            continue
        elif i == '日增长率':
            continue
        elif i == '申购状态':
            continue
        elif i == '赎回状态':
            continue
        elif i == '红送配':
            continue
        elif i == '                            ':
            continue
        elif i == '开放申购':
            continue
        elif i == '开放赎回':
            continue
        elif i == '限制大额申购':
            continue
        elif i == '每份派现金0.0860元':
            continue
        elif i == '分红送配':
            continue
        elif i == '                      ':
            continue

        else:
            result_data.append(i)
#print(result_data)
#创建四个列表，收集对应数据。
data_date = ['净值日期']
data_Net_unit_value = ['单位净值']
data_Cumulative_net_worth = ['累计净值']
data_Daily_growth_rate = ['日增长率']
step = 0
for i in result_data:
    if step % 4 == 0:
        data_date.append(i)
    if step % 4 == 1:
        data_Net_unit_value.append(i)
    if step % 4 == 2:
        data_Cumulative_net_worth.append(i)
    if step % 4 == 3:
        data_Daily_growth_rate.append(i)
    step += 1
print(data_date)
print(data_Net_unit_value)
print(data_Cumulative_net_worth)
print(data_Daily_growth_rate)





