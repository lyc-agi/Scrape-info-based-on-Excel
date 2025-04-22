# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# # 配置
# INPUT_EXCEL = "极速导入.xlsx"
# OUTPUT_EXCEL = "查询结果.xlsx"
# KEYWORD_COLUMN = "产品"
# COMPANY_COLUMN = "公司"
# SLEEP_TIME = 2
#
# # 请求百度搜索
# def search_baidu(keyword):
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#     search_url = f"https://www.baidu.com/s?wd={keyword}"
#     try:
#         response = requests.get(search_url, headers=headers)
#         response.raise_for_status()
#
#         # 使用 BeautifulSoup 解析 HTML
#         soup = BeautifulSoup(response.text, "html.parser")
#         result = soup.find("div", class_="result")
#         if result:
#             return result.get_text(strip=True)
#         else:
#             return "未找到摘要"
#     except Exception as e:
#         return f"请求失败: {e}"
#
# # 读取 Excel
# df = pd.read_excel(INPUT_EXCEL)
# df["查询关键词"] = df.apply(lambda row: f"{row[KEYWORD_COLUMN]} {row[COMPANY_COLUMN]}", axis=1)
#
# # 批量处理搜索
# results = []
# for idx, keyword in enumerate(df["查询关键词"]):
#     print(f"[{idx+1}/{len(df)}] 正在搜索：{keyword}")
#     result = search_baidu(keyword)
#     results.append(result)
#     time.sleep(SLEEP_TIME)
#
# # 写入结果
# df["搜索结果"] = results
# df.to_excel(OUTPUT_EXCEL, index=False)
# print(f"\n✅ 查询完成，结果已保存到：{OUTPUT_EXCEL}")

import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 配置
CHROMEDRIVER_PATH = "D:/chromedriver/chromedriver.exe"
INPUT_EXCEL = "极速导入.xlsx"
OUTPUT_EXCEL = "查询结果.xlsx"
KEYWORD_COLUMN = "产品"
COMPANY_COLUMN = "公司"
SLEEP_TIME = 2


# 启动 WebDriver
def start_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)


# 自定义搜索函数
def search_baidu(keyword):
    driver = start_driver()
    driver.get("https://www.baidu.com")
    search_box = driver.find_element_by_id("kw")
    search_box.send_keys(keyword)
    search_box.submit()
    time.sleep(SLEEP_TIME)

    try:
        result = driver.find_element_by_css_selector("div.result, div.c-container").text
    except Exception as e:
        result = f"错误: {e}"
    driver.quit()
    return result


# 读取 Excel
df = pd.read_excel(INPUT_EXCEL)
df["查询关键词"] = df.apply(lambda row: f"{row[KEYWORD_COLUMN]} {row[COMPANY_COLUMN]}", axis=1)


# 使用多线程执行搜索
def process_rows():
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(search_baidu, df["查询关键词"]))
    return results


# 执行爬取并保存
results = process_rows()
df["搜索结果"] = results
df.to_excel(OUTPUT_EXCEL, index=False)
print("✅ 查询完成，结果已保存到：", OUTPUT_EXCEL)
