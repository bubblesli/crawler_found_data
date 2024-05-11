import requests
from bs4 import BeautifulSoup
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/your_chrome_version Safari/537.36',
}
fund_url = "https://fundf10.eastmoney.com/jjjz_002583.html"
# 发送请求
response = requests.get(fund_url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
reselt = soup.find_all(class_='title')
for i in reselt[0]:
    for y in i :
        s = str(y)
        print(s)
#print(reselt)