
# importing libraries:
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd

# Setting up the chrome driver:
from selenium.webdriver.chrome.service import Service
ser = Service("/Users/AnaPSilva/Documents/Ana/Ironhack/Bootcamp/Week3/Project3- Streaming/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

# Scraping HBO Portugal:
website = 'https://hboportugal.com/'
driver.get(website)

## Changing the page from Portuguese to English
english_button3 = driver.find_element(By.CSS_SELECTOR,'body > div.footer > nav.footer-links > ul > li.region-container > span > span')
english_button3.click()
time.sleep(2)
english_button4 = driver.find_element(By.CSS_SELECTOR,'body > div.footer > nav.footer-links > ul > li.region-container > span > ul > li:nth-child(2) > a')
english_button4.click()
time.sleep(2)


## Going to the MOVIES general page
all_movies_button = driver.find_element(By.XPATH,'//a[@href="/movies"]')
all_movies_button.click()

# Finding the movie names location
all_movies_hbo = driver.find_elements(By.XPATH,'//span[@class="title"]')

# Web Scraping all movie names into a list
movies_names = []
for movie in range(len(all_movies_hbo)):
    movies_names.append(all_movies_hbo[movie].text)
print(movies_names)


## Going to the SERIES general page
series_button = driver.find_element(By.XPATH,'//a[@href="/series"]')
series_button.click()

# Finding the series names location
series_hbo = driver.find_elements(By.XPATH,'//span[@class="title"]')

# Web Scraping all series names into a list
series_names = []
for serie in range(len(series_hbo)):
    movies_names.append(series_hbo[serie].text)
print(movies_names)

hbo_movies_series = pd.DataFrame(movies_names)
hbo_movies_series.to_csv('hbo_shows_movies.csv',index=False)