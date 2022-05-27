import random
import requests
import json
from bs4 import BeautifulSoup

def getImdbFilms():
    imdburl = "https://www.imdb.com/chart/top/"
    header={"accept-language":"tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"}
    r=requests.get(imdburl,headers=header)

    soup = BeautifulSoup(r.content,"html.parser")

    get_data=soup.find_all("table",{"class":"chart full-width"})
    film_table = (get_data[0].contents)[len(get_data[0].contents)-2]
    film_table = film_table.find_all("tr")
    # f = open("C:/Users/hupes/Desktop/IMDBTOP250","w")

    imdbFilms = []
    for film in film_table:
        filmbasliklar = film.find_all("td",{"class":"titleColumn"})
        film_name=film.find_all("a")[1].text
        # film_name=filmbasliklar[0].tex
        # film_name=film_name.replace("\n","")
        imdbFilms.append(film_name)

    return imdbFilms


def get_movie(number):

    start = requests.get(f"https://api.mubi.com/v3/lists/the-top-1000/list_films", headers = {
        'authority': 'api.mubi.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'anonymous_user_id': 'fe7c0cdf-7fed-4224-89e6-0a3a5b3069e5',
        'client': 'web',
        'client-accept-video-codecs': 'vp9,h264',
        'client-country': 'IN',
        'origin': 'https://mubi.com',
        'referer': 'https://mubi.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'x-forwarded-for': '223.228.133.79, 223.228.133.79',
        'x-forwarded-proto': 'https',
        'x-real-ip': '223.228.133.79',
    },
     params={
         'page': f'{(number-1)//200 + 1}',
         'per_page': '200',
     }
    )

    movies = [i['film']['title'] + f"({str(i['film']['year'])})" for i in json.loads(start.content)['list_films']]
    movies.extend(getImdbFilms())
    return movies


MOVIES = get_movie(random.randint(1, 1000))

print(random.choice(MOVIES))
