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
import re

def get_id(fund_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/your_chrome_version Safari/537.36',
    }
    # 发送请求
    response = requests.get(fund_url, headers=headers)
    # 检查响应状态码是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        reselt = soup.find_all(class_='title')
        name_id = ''
        for i in reselt[0]:
            for y in i:
                name_id += str(y)
            # 输出或处理提取的数据
        return name_id
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None

def web_drive(driver,fund_url, data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate):
    while True:
        try:
            grouped_data = get_data(driver)
            try:
                result_data = process_data(grouped_data)
                print(result_data)
            except IndexError as e:
                print(f"发生错误：{e}，数据未加载完完成，等待加载.........")
                continue
            data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate = split_data(result_data, data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate)
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='pagebar']/div[1]/label[8]"))
            )
            next_button.click()
            time.sleep(0.05)

        except TimeoutError as e:
            print(f"发生错误，已跳过，错误详情：{e}")
            continue
        except TimeoutException as te:
            fund_url_id = fund_url
            #global data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate
            save_data(data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate, fund_url_id)
            break
    # 关闭浏览器
    driver.quit()

def get_data(driver):
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
    return grouped_data
def process_data(grouped_data):
    result_data = []
    date_pattern = r'\d{4}-\d{2}-\d{2}' #日期
    float_pattern = r'\d+\.\d+' # 浮点
    negative_percent_pattern = r'-?\d+(\.\d+)?%' #百分号
    pattern_ch = r'[\u4e00-\u9fff]+' #汉字
    #patterns = [date_pattern, float_pattern, float_pattern, negative_percent_pattern]
    #print(result_data)
    for sublist in grouped_data[0]:
        lines = sublist.split('\n')
        for i in lines:
            if re.search(date_pattern, i) != None:
                result_data.append(i)
            elif re.search(float_pattern, i) != None and re.search(pattern_ch,i) == None:
                result_data.append(i)
            elif re.search(negative_percent_pattern, i) != None:
                result_data.append(i)
            elif re.search(pattern_ch, i) != None:
                continue
            elif i == '--':
                result_data.append('0.00%')
            else:
                continue
            """
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
            elif i == '暂停申购':
                continue
            elif i == '暂停赎回':
                continue
            elif '收益' or '*' in i:
                continue
            else:
                result_data.append(i)
           """


    return result_data
def split_data(result_data,data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate):

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
    return data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate

def save_data(data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate, fund_url):
    # 创建一个DataFrame，将这些列表作为列
    df = pd.DataFrame(list(zip(data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate)),
                      columns=['净值日期', '单位净值', '累计净值', '日增长率'])
    fund_url_id = fund_url
    name_id = get_id(fund_url_id)
    save_path = './data/'
    # 写入CSV文件
    try:
        df.to_csv(save_path+name_id, index=False, encoding='utf-8')
        print('写入完成')
    except FileNotFoundError as e:
        print(f"发生错误{e},已跳过")
        return


def web_dfing(fund_url):
    chrome_exe_path = r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    # 创建浏览器实例
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
    return driver
def run():
    # 目标基金URL
    e = int("011030")
    format_string = '{:06d}'
    while True:
        url = f'https://fundf10.eastmoney.com/jjjz_{e}.html'
        print(url)
        fund_url = test_id(url)
        if fund_url == 200:
            driver = web_dfing(url)
            data_date = []
            data_Net_unit_value = []
            data_Cumulative_net_worth = []
            data_Daily_growth_rate = []
            web_drive(driver, url, data_date, data_Net_unit_value, data_Cumulative_net_worth, data_Daily_growth_rate)
            e = int(e)
            e += 1
            e = format_string.format(e)
            print(e)

        else:
            e = int(e)
            if e < 591000:
                e += 1
                e = format_string.format(e)
                print(e)
            else:
                break
def test_id(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/your_chrome_version Safari/537.36',
    }
    # 发送请求
    response = requests.get(url, headers=headers)
    # 检查响应状态码是否成功
    return response.status_code


if __name__ =='__main__':
    run()





