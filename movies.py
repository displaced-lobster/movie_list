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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import shelve

def isFloat(num):
    try:
        float(num)
        return True
    except:
        return False

def imdbData(movie, year):
    url = 'http://www.omdbapi.com/?t='
    endUrl = '&y=' + year + '&plot=short&r=json'
    urlSearch = url + movie.replace(" ", "+") + endUrl
    resp = requests.get(url = urlSearch)
    data = json.loads(resp.text)
    if data['Response'] == 'True':
        rating = data['imdbRating']
        if isFloat(rating):
            if float(rating) >= 7.0:
                link = "www.imdb.com/title/" + data['imdbID']
                return [movie, rating, link, data['Plot']]
    return -1

def email(subject, text, html):
    d = shelve.open('email_helper')
    username = d['from_address']
    password = d['password']
    toAddresses = d['to_addresses']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = ', '.join(toAddresses)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com:587') # Change if not using gmail
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(username, toAddresses, msg.as_string())
    server.quit()
    return

source = urllib.request.urlopen('http://www.edmovieguide.com/movies/?sort=release-date')
soup = bs.BeautifulSoup(source, 'lxml')
movie_list = []

for li in soup.find_all('li', class_ = 'movie'):
    for a in li.find_all('a', class_ = 'movie-title'):
        movie_name = a.text
    for p in li.find_all('p', class_ = 'movie-date'):
        movie_date = p.text[-4:]

    movie_list.append([movie_name, movie_date])

goodMovies = []

for movie in movie_list:
    movieData = imdbData(movie[0], movie[1])
    if movieData != -1:
        goodMovies.append(movieData)

movieText = ''
movieHTML = ''

for movie in goodMovies:
    movieText += movie[0] + '     ' + movie[1] + '\n'
    movieText += movie[3] + '\n'
    movieHTML += '<tr><td><a href="%s">%s</a></td>' %(movie[2], movie[0])
    movieHTML += "<td>%s</td></tr>" %movie[1]
    movieHTML += "<tr><td>%s</td></tr>" %movie[3]

text = "Top Rated Movies Playing in Edmonton!\n\n%s" %movieText
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
""" %movieHTML

email(toAddresses, "Movie List", text, html)
