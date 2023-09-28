import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import json

from sys import stdout as terminal
from time import sleep
from itertools import cycle
from threading import Thread
from colorama import Fore as F
import random

done = False
def animate():
    for a in (cycle(['|', '/', '-', '\\'])):
        if done:
            break
        terminal.write('\033[1m' + random.choice([F.CYAN, F.GREEN, F.YELLOW, F.MAGENTA]) + '\rCrawling ' + a + '\033[0m')
        terminal.flush()
        sleep(0.1)
    terminal.write('\rDone!    ')
    terminal.flush()

t = Thread(target=animate)
t.start()

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
pattern_api = "https://caching.graphql.imdb.com/?operationName=TMD_Storyline&variables=%7B%22isAutoTranslationEnabled%22%3Afalse%2C%22locale%22%3A%22en-US%22%2C%22titleId%22%3A%22tt{id}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%22ad739d75c0062966ebf299e3aedc010e17888355fde6d0eee417f30368f38c14%22%2C%22version%22%3A1%7D%7D"
headerss = {"Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "en-US,en;q=0.9,fa;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36'}
response = requests.get(url, headers=headerss)
# print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
li_movie = soup.find('ul', {'class': 'ipc-metadata-list ipc-metadata-list--dividers-between sc-3f13560f-0 sTTRj compact-list-view ipc-metadata-list--base'})
# print(li_movie)
movies = li_movie.find_all('div', {'class': 'ipc-metadata-list-summary-item__tc'})

movie_id = []
title = []
year = []
parental = []
duration = []
genres = []
context = []
director = []
id_director = []
writers = []
ids_writer = []
stars = []
ids_star = []

gross_us_canada = []


counter = 0
for movie in movies:
    counter += 1
    if counter%50 == 0:
        print('\n',counter)
        # break
    single_movie = movie.find('a', href=True)
    pattern = r"/title/tt(\d+)/"
    match = re.search(pattern, single_movie['href'])
    idd = str(match.group(1))
    url = re.sub("{id}", idd, pattern_api)
    # movie_id.append(url)
    api_res = requests.get(url, headers=headerss)
    data = json.loads(api_res.text)
    plot_data = data['data']['title']['summaries']['edges'][0]['node']['plotText']
    # print(plot_data['plaidHtml'])
    context.append(plot_data['plaidHtml'])
    movie_link = 'https://www.imdb.com/' + single_movie['href']
    movie_link = 'https://www.imdb.com/title/tt9362722/?ref_=chttp_t_18'
    mov_res = requests.get(movie_link, headers=headerss)
    movie_details = BeautifulSoup(mov_res.text, 'html.parser')
    title.append(movie_details.find('span', {'class': 'sc-afe43def-1 fDTGTb'}).text)
    ################################
    #year and parent and duration
    min_det = movie_details.find('ul', {'class': 'ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt'})
    full_text = ''
    boolin = False
    if len(min_det) < 3:
        boolin = True

    for i in min_det:
        full_text += i.text + '|'
    nothing = full_text.split('|')

    if boolin:
        year.append(int(nothing[0]))
        parental.append('Unrated')
        run_str = nothing[1]
        run_str = run_str.replace('h', '').replace('m', '').strip()
        total_minutes = int(run_str[0]) * 60 + 0 if run_str[1:] == '' else int(run_str[1:])
        duration.append(total_minutes)
    else:
        year.append(int(nothing[0]))
        if nothing[1] == 'Not Rated':
            parental.append('Unrated')
        else:
            parental.append(nothing[1])
        run_str = nothing[2]
        run_str = run_str.replace('h', '').replace('m', '').strip()
        total_minutes = (int(run_str[0]) * 60) + (0 if run_str[1:] == '' else int(run_str[1:]))
        duration.append(total_minutes)
    # print(duration)

    ################################
    gens = movie_details.find('div', {'class': 'ipc-chip-list__scroller'}).text
    pattern = r'[A-Z][^A-Z]*'
    # gens = re.findall(pattern, gens)
    genres.append(re.findall(pattern, gens))
    ################################
    ul_stars = movie_details.find('ul', {'class': 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt'})
    pattern = r"/name/nm(\d+)/"
    person_d = []
    person_w = []
    person_s = []
    ids_d = []
    ids_w = []
    ids_s = []
    for attemplate in ul_stars:
        charr = attemplate.text[0]

        if 'D' == charr:
            for direc in attemplate.find('ul', {'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt'}):
                person_d.append(direc.find('a', href=True).text)
                str_href = direc.find('a', href=True)['href']
                match = re.search(pattern, str_href)
                if match:
                    ids_d.append(match.group(1))
        elif 'W' == charr:
            for writer in attemplate.find('ul', {'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt'}):
                person_w.append(writer.find('a', href=True).text)
                str_href = writer.find('a', href=True)['href']
                match = re.search(pattern, str_href)
                if match:
                    ids_w.append(match.group(1))
        else:
            for star in attemplate.find('ul', {'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt'}):
                person_s.append(star.find('a', href=True).text)
                str_href = star.find('a', href=True)['href']
                match = re.search(pattern, str_href)
                if match:
                    ids_s.append(match.group(1))

    id_director.append(ids_d)
    ids_writer.append(ids_w)
    ids_star.append(ids_s)
    director.append(person_d)
    writers.append(person_w)
    stars.append(person_s)

    ################################
    try:
        box_off = movie_details.find('div', {"class": 'sc-c7c3a435-1 NixYx ipc-page-grid__item ipc-page-grid__item--span-2'})
        guc = box_off.find('li', {'data-testid': 'title-boxoffice-grossdomestic'})
        sell = int(guc.find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.replace(',', '').replace('$', ''))
        gross_us_canada.append(sell)
    except Exception:
        gross_us_canada.append(np.nan)

    sleep(.75)

done = True

# print(
#     'movie_id :' ,len(movie_id),
#     'title :' ,len(title),
#     'year :' ,len(year),
#     'parental :' ,len(parental),
#     'runtim :', len(duration),
#     'genre :' ,len(genres),
#     'id_director :' ,len(id_director),
#     'director :' ,len(director),
#     'ids_writer :' ,len(ids_writer),
#     'writers :' ,len(writers),
#     'ids_stars :' ,len(ids_star),
#     'stars :' ,len(stars),
#     'gus :' ,len(gross_us_canada)
#     )

df_movie = pd.DataFrame({
    'movie_id' : movie_id,
    'title' : title,
    'year' : year,
    'parental' : parental,
    'runtime' : duration,
    'genre' : genres,
    'id_director' : id_director,
    'director' : director,
    'ids_writer' : ids_writer,
    'writers' : writers,
    'ids_stars' : ids_star,
    'stars' : stars,
    'gus' : gross_us_canada
})
df_con = pd.DataFrame({'context' : context})

df_con.to_csv('con.csv', index=False)

