import time
from urllib import response
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

game_list = {}

URL = "https://store.steampowered.com/search/?category1=998&filter=topsellers"


chrome_options=webdriver.ChromeOptions()
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(URL)

last_page_height = driver.execute_script(
    "return document.documentElement.scrollHeight")

while True:
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.0)
    new_page_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    if new_page_height == last_page_height:
        time.sleep(1.0)
        if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
            break
    else:
        last_page_height = new_page_height

response = requests.get(driver.current_url, cookies={
    'Steam_Language': 'koreana'
})
response.raise_for_status()

soup = BeautifulSoup(driver.page_source, "html.parser")

atags = soup.select('a.search_result_row')
titles = soup.select('.col.search_name.ellipsis .title')


print("title 개수 :", len(titles))

id_list = []
title_list = []
for atag, title in zip(atags, titles):
    idtag = atag.attrs['data-ds-appid']

    if "," in idtag:
        idtag = idtag.split(",")[0]

    title = title.text

    id_list.append(idtag)
    title_list.append(title)

id_df = pd.DataFrame(
    {
        'id': id_list,
        'title': title_list
    }
)

id_df.to_csv('id_test.csv')

