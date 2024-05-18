from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_argument("--disable-images")
PREFS = {"profile.managed_default_content_settings.images": 2}
CHROME_OPTIONS.add_experimental_option("prefs", PREFS)

URL = 'https://scpsandboxcn.wikidot.com/pagelisttest' #检测的Listpage页面
DELAY = 120 #检测间隔时间
FILENAME_OLD = "data.txt"
FILENAME_NEW = "newdata.txt"

def saomiao(filename):
    print("开始扫描并存储至", filename)
    if os.path.exists(filename):
        os.remove(filename)
    
    try:
        with webdriver.Chrome(options=CHROME_OPTIONS) as driver:
            driver.get(URL)
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'list-pages-item')))
            items = driver.find_elements(By.CLASS_NAME, 'list-pages-item')
            with open(filename, 'a', encoding='utf-8') as file:
                for item in items:
                    link_element = item.find_element(By.TAG_NAME, 'a')
                    link = link_element.get_attribute('href')
                    p_text = item.find_element(By.TAG_NAME, 'p').text
                    parts = p_text.split('\n')
                    page_name = parts[0]
                    author = parts[1] if len(parts) >= 2 else "未知作者"
                    date_element = item.find_element(By.CLASS_NAME, 'odate')
                    date = date_element.get_attribute('innerText')
                    file.write(f"{page_name},{link},{author},{date}\n")
        print("扫描已完成，已存储结果至", filename)
    except Exception as e:
        print(f"扫描过程中出现错误: {e}")

def find_extra_lines(file1, file2):
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            lines1 = set(' '.join(line.split()) for line in f1.readlines())
        with open(file2, 'r', encoding='utf-8') as f2:
            lines2 = [' '.join(line.split()) for line in f2.readlines()]
        extra_lines = [line for line in lines2 if line not in lines1]
        if extra_lines:
            for line in extra_lines:
                print(line)
        else:
            print("无更新")
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")

def main_loop():
    while True:
        saomiao(FILENAME_OLD)
        print(f"等待{DELAY}秒后再次检测...")
        time.sleep(DELAY)
        saomiao(FILENAME_NEW)
        print("开始对比")
        find_extra_lines(FILENAME_OLD, FILENAME_NEW)

if __name__ == "__main__":
    main_loop()
