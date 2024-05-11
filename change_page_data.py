from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import TimeoutException
import requests
fund_url = "https://fundf10.eastmoney.com/jjjz_002583.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/your_chrome_version Safari/537.36',
}
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
driver.get(fund_url)
time.sleep(3)
# 创建四个列表，收集对应数据。
data_date = []
data_Net_unit_value = []
data_Cumulative_net_worth = []
data_Daily_growth_rate = []
while True:
    try:

        html_content = driver.page_source
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
        try:
            for sublist in grouped_data[0]:
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
                    elif '每份派' in i:
                        continue
                    else:
                        result_data.append(i)
                break
        except IndexError as e:
            print(f"f:发生错误，已跳过，错误：{e}")
            continue
        # print(result_data)

        step = 0
        for i in result_data:
            if step % 4 == 0:
                data_date.append(i)
            if step % 4 == 1:
                data_Net_unit_value.append(i)
            if step % 4 == 2:
                data_Cumulative_net_worth.append(i)
            if step % 4 == 3:
                if i == '--':
                    break
                data_Daily_growth_rate.append(i)
            step += 1
        print(data_date)
        print(data_Net_unit_value)
        print(data_Cumulative_net_worth)
        print(data_Daily_growth_rate)
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='pagebar']/div[1]/label[8]"))
        )
        next_button.click()
    except TimeoutError as e:
        print(f"发生错误，已跳过，错误详情：{e}")
        continue
    except TimeoutException as te:
        # 创建一个DataFrame，将这些列表作为列
        df = pd.DataFrame(list(zip(data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate)),
                          columns=['净值日期', '单位净值', '累计净值', '日增长率'])
        response = requests.get(fund_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        reselt = soup.find_all(class_='title')
        name_id = ''
        for i in reselt[0]:
            for y in i:
                name_id += str(y)
        # 写入CSV文件
        df.to_csv(name_id, index=False, encoding='utf-8')
        print('写入完成')
        break

#关闭浏览器
driver.quit()
