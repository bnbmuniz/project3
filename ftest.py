import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import requests
import time
import random
import re
from dateutil import parser
from apiclient.discovery import build
import requests
import webbrowser

api_key = "AIzaSyA9Tb_efqIGXwKaDmZWN2nz5kXw_Qg1cmI"

# Load dataset that is already clean
imdb = pd.read_csv('1imdb_final.csv', index_col=False)

imdb.drop(columns='Unnamed: 0', inplace=True)




def changing_time(row):
    if ":" in row:
        ti_li=row.split(":")
        if len(ti_li[1])!=1:
            row = (int(ti_li[0])*60)+int(ti_li[1])
            return row 
        elif len(ti_li[1])==1:
            row = (int(ti_li[0])*60)+(int(ti_li[1])*10)
            return row
    elif len(row)==1:
        return int(row)*60
    else:
        return int(row)

def get_time(user_input):
    if ':' in user_input:
        hour = int(parser.parse(user_input).hour)
        min = int(parser.parse(user_input).minute)
        total_time = hour * 60 + min

    elif ('h' in user_input) & ('m' in user_input):
        user_input = re.sub('m.*', 'm', user_input)
        hour = int(parser.parse(user_input).hour)
        min = int(parser.parse(user_input).minute)
        total_time = hour * 60 + min

    elif 'h' in user_input:
        if user_input.index('h') != user_input[-1]:
            hour = int(parser.parse(user_input).hour)
            min = int(parser.parse(user_input).minute)
            total_time = hour * 60 + min
        else:
            hour = int(parser.parse(user_input).hour)
            total_time = hour * 60

    elif 'm' in user_input:
        user_input = re.sub('m.*', 'm', user_input)
        min = int(parser.parse(user_input).minute)
        total_time = min

    elif ((len(user_input) > 1) |(len(user_input) == 1)) & (re.search('[a-zA-Z]', user_input) == None):
        what = input("do you mean hours or min: ").strip()[0]
        if what == 'h':
            hour = int(user_input)
            total_time = hour * 60
        else:
            min = int(user_input)
            total_time = min
    return total_time

imdb['duration_min'] = imdb['duration'].apply(changing_time)

imdb = imdb[['type',"title", "director", "duration", 'duration_min', 'genre', 
             'hbo','disney+', 'netflix', 'rating']]

def time4():
    # Define inputs
    a = input('How much time for a good time do you have? ').lower().strip().replace(' ', '')
    time_input = get_time(a)
    platform_input = input("Which platform you use? HBO, Netflix, Disney+").lower().strip()
    genre_input = input('What do you feel like watching? ').capitalize().strip()

    # Filter the df according to the inputs
    select_genre = imdb['genre'].str.contains(f'{genre_input}', na=False)
    select_dur = imdb['duration_min'] <= int(time_input)
    select_platform = imdb[f'{platform_input}'] == 'Yes'
    
    # Output top10
    selection = imdb[(select_genre) & (select_dur) & (select_platform)]
    selection = selection.sort_values(by='rating', axis=0, ascending=False).head(10)
    return selection.reset_index().drop(columns='index')


youtube = build('youtube','v3',developerKey = api_key)

def get_trailer(movie_show):
    trail = input('Do you want to watch the trailer? ').lower()
    if (trail == 'yes') | (trail == 'y'):
        request = youtube.search().list(q=f'{movie_show}+trailer',part='snippet',type='video')
        res = request.execute()
        video_id = res['items'][0]['id']['videoId']
        url_yt = f'https://www.youtube.com/watch?v={video_id}'
        print(url_yt)
        return webbrowser.open_new(url_yt)
    elif (trail == 'no') | (trail == 'n'):
        print('Enjoy your time! See you next time')
    else:
        print('Try again')
        get_trailer(movie_show)



movie_table = time4()
while movie_table.shape[0] == 0:
        print('No movies. Try again')
        movie_table = time4()
else:
    print(movie_table)
    movie = input('Which one you wanna watch? ')
    get_trailer(movie)