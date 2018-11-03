import requests
import pymysql
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from requests.exceptions import RequestException
from time import sleep
import os

baseurl = 'https://tw.manhuagui.com'
response = requests.get('https://tw.manhuagui.com/comic/8150/')
urllist = []
titlelist = []
bs = BeautifulSoup(response.text, 'lxml')
div = bs.find_all(id='chapter-list-0')[0]
titles = re.findall('title="(.*?)"', str(div))
for title in titles:
    titlelist.insert(0, title)
urls = re.findall('href="(.*?)"', str(div))
for url in urls:
    url = baseurl + url
    urllist.insert(0, url)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
driver.get('https://tw.manhuagui.com/comic/8150/')


def open_url(url):
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mangaFile')))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#next")))
        num = re.search('</span>/(\d+)\)</span>',driver.page_source,re.S).group(1)
        return int(num)
    except TimeoutException:
        open_url(url)


def next_page():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mangaFile')))
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#next"))
        )
        button.click()
    except TimeoutException:
        next_page()
    except StaleElementReferenceException:
        next_page()


def get_img():
    html = driver.page_source
    doc = pq(html)
    img = doc('.mangaFile').attr('src')
    page = doc('#page').text()
    return page, img


def save_img(imgurl, page, referer, seal):
    headers = {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    filename = 'citrus/' + seal + '/' + page + '.webp'
    if not os.path.exists('citrus/'+seal+'/'):
        os.makedirs('citrus/'+seal)
    try:
        response = requests.get(imgurl, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
                f.close()
                return print('保存成功')
        return None
    except RequestException:
        print('请求图片出错了')
        return None


def main(seal, url):
    num = open_url(url)
    referer = url
    for i in range(0, num):
        page, img = get_img()
        save_img(img, page, referer, seal)
        next_page()


if __name__ == '__main__':
    for i in range(0, len(urllist)):
        main(titlelist[i], urllist[i])

