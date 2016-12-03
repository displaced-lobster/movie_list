#!/usr/bin/env python3
#-----------------------------------------------------------------------------------
# movies.py
# v1.1
# by Richard Mills
# Scrapes website for movies playing in Edmonton, fetches IMDB rating and compiles list of high rated movies. Emails list
#-----------------------------------------------------------------------------------

import bs4 as bs
import urllib.request
import json
import requests

import gmail_helper

def isFloat(num):
    try:
        float(num)
        return True
    except:
        return False

def imdbData(movie, year):
    url = 'http://www.omdbapi.com/?t='
    end_url = '&y=' + year + '&plot=short&r=json'
    url_search = url + movie.replace(" ", "+") + end_url
    resp = requests.get(url = url_search)
    data = json.loads(resp.text)
    if data['Response'] == 'True':
        rating = data['imdbRating']
        if isFloat(rating):
            if float(rating) >= 7.0:
                link = "www.imdb.com/title/" + data['imdbID']
                return [movie, rating, link, data['Plot']]
    return -1

def main ():
    source = urllib.request.urlopen('http://www.edmovieguide.com/movies/?sort=release-date')
    soup = bs.BeautifulSoup(source, 'lxml')
    movie_list = []

    for li in soup.find_all('li', class_ = 'movie'):
        try:
            movie_name = li.find('a', class_ = 'movie-title').text
            try:
                movie_date = li.find('p', class_ = 'movie-date').text[-4:]
            except:
                movie_date = ''
            movie_list.append([movie_name, movie_date])
        except:
            pass

    good_movies = []

    for movie in movie_list:
        movie_data = imdbData(movie[0], movie[1])
        if movie_data != -1:
            good_movies.append(movie_data)

    movie_text = ''
    movie_HTML = ''

    for movie in good_movies:
        movie_text += movie[0] + '     ' + movie[1] + '\n'
        movie_text += movie[3] + '\n'
        movie_HTML += '<tr><td><a href="%s">%s</a></td>' %(movie[2], movie[0])
        movie_HTML += "<td>%s</td></tr>" %movie[1]
        movie_HTML += "<tr><td>%s</td></tr>" %movie[3]

    text = "Top Rated Movies Playing in Edmonton!\n\n"
    text += movie_text
    html = """\
    <html>
        <head></head>
        <body>
            <h1>Top Rated Movies Playing in Edmonton!</h1>
            <br>
            <table>
                <tr><th>Movie</th><th>Rating</th></tr>
                %s
            </table>
        </body>
    </html>
    """ %movie_HTML

    with open('emails.txt') as f:
        emails = f.read().splitlines()

    sender = emails.pop(0)

    gmail_helper.email(sender, emails, 'Movie List', text, html)
