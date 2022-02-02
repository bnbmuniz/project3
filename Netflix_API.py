#Libraries to import
import pandas as pd
import requests
import time
import random
from bs4 import BeautifulSoup
import re



titles_list=[]

try:
#finding the fisrt 5 urls to test it    
    for number in range(1,20):
        url = 'https://www.flixwatch.co/catalogue/netflix-portugal/?paged='+str(number)
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
#to imitate a human we use time
        time.sleep(random.randint(2,6))
#finding only the title names
        titles = soup.find_all('div', attrs={'class':'item-title'})
        for title in titles:
            titles_list.append(title.text)

                
except:
    pass

col = ['Netflix Tiles']
titles_df = pd.DataFrame(titles_list, columns = col)



def cleaning(row):
#this function cleans the titles
    for element in row:
        element = element.lower().replace(":", "")
        element = element.replace("’","")
        element = element.replace("(", "")
        element = element.replace(")", "")
        element = element.replace("°","")
        element = element.replace("º","")
        element = element.replace("?","")
        element = element.replace("!","")
        element = element.replace(",", "")

        return element

titles_df['Cleaned titles'] = titles_df.apply(cleaning, axis=1)
print(titles_df)

titles_df.to_csv('/Users/barbaramuniz/Documents/Ironhack_FullTime/Projects/Project3_API:Webscraping/titles.csv', index=False)
#titles_read = pd.read_csv('titles.csv')
#print(titles_read)
