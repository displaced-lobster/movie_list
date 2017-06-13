# Scrapes Website For Movies Playing in Edmonton

Using BeautifulSoup, edmontonmoveguide.com is scraped for a list of movies
playing in Edmonton. Then using The Movie Database, ratings are fetched to compile
a list of 'high' rated movies to be sent out to via email.

## Usage
The script expects an 'emails.txt' file to be present in the same folder.
This file contains a newline separated list of emails. The first email is the
sender and the remaining are receivers.

## Note:
Emails are sent using my gmail_helper script which has been modified slightly
from the Gmail API tutorials.

This product uses the TMDb API but is not endorsed or certified by TMDb.
