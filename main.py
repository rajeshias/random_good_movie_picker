import random
import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

def getImdbFilms():
    imdburl = "https://www.imdb.com/chart/top/"
    headers = {
    'authority': 'www.imdb.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id-time=2082787201l; session-id=135-0705048-9484236; ubid-main=133-8806051-1324352; uu=eyJpZCI6InV1Y2Y1NWI5MGY3OGQxNGRmZmJkOGQiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfX0=; session-token=ozSIsIJ8AE833+CCghVPuOnDJaNracIeWCSPqhpMhm4n9qFZ2rfMy8nCyU8FgKaCBVXpe9+qLylkxbxBRjnD2+Ymucce8HuQBinghEmoG4RfN+kP0hyAWVmanu1G9pOPvTphQ1WD2NaBO9Hb3pCV49C8fPDY05CEmcPuAXp0Szx4aMPUSaA1wRNDuqFhIt1T6w5oRCaLKUch0eWa0QGy1ecmU0cZpz9VLoK/tkwdR1MkMGAnaOVm3e8E09p0WJ7sISy/b9zTVhjnwsrJX3DEiIRiIh9wpmpjlLwPuuXmE210GO31MI5OBzYyDjnw79EA2vzeBJrBQ7glVkvvqLybWlboeXxZgEqf; csm-hit=tb:ES1MKHCEA8B91HBZHJ8C+s-ES1MKHCEA8B91HBZHJ8C|1709689788520&t:1709689788520&adb:adblk_yes; ad-oo=0; ci=e30',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}
    r=requests.get(imdburl,headers=headers)

    soup = BeautifulSoup(r.content,"html.parser")
    film_list=soup.find_all("div",{"class":"srahg"})
    # f = open("C:/Users/hupes/Desktop/IMDBTOP250","w")

    imdbFilms = []
    for film in film_list:
        # filmbasliklar = film.find_all("td",{"class":"titleColumn"})
        film_name=film.text
        # film_name=filmbasliklar[0].tex
        # film_name=film_name.replace("\n","")
        imdbFilms.append(f"imdb#{film_name}")
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
    print(len(movies))
    return movies

# create a json file that holds a list of watched movies and add the movie to the list after user confirms as watched 
# if the movie is already in the list, then go to the next loop
# if the movie is not in the list, then add it to the list and ask the user if they have watched it


watched = []
#if file does not exist, create it
try:
    with open('watched.json', 'r') as f:
        watched = json.load(f)
except FileNotFoundError:
    with open('watched.json', 'w') as f:
        json.dump(watched, f, indent=4)

movies = get_movie(random.randint(1, 1000))
while True:
    selectedMovie = random.choice(movies)
    if selectedMovie in watched:
        continue
    with open('watched.json', 'w') as f:
        json.dump(watched, f, indent=4)
    if input(f"\nHave you watched {selectedMovie}? (y/n): ") == 'y':
        watched.append(selectedMovie)
        continue
    else:
        break
