import xml

from html.parser import HTMLParser
import regex
import requests
from bs4 import BeautifulSoup
import re

source = requests.get("https://www.imdb.com/search/title/?genres=comedy").text
soup = BeautifulSoup(source, "lxml")
ratings=[]
for article in soup.find_all("div", class_="lister-item-content")[:5]:
    headline = article.h3.a.text
    summary = article.find_all("p", class_="text-muted")[1].text
    movie_launch = article.find("span", class_="lister-item-year text-muted unbold").text[1:5]
    movie_duration = article.find("span", class_="runtime")
    movie_rating = article.find("strong")
    ratings.append(movie_rating)
    director = article.find_all("p")[2]("a")[0].text
    star1 = article.find_all("p")[2]("a")[1].text
    star2 = article.find_all("p")[2]("a")[2].text
    star3 = article.find_all("p")[2]("a")[3].text
    print(headline, summary, movie_launch, movie_duration, movie_rating, director, star1, star2, star3)


'''
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed('<strong>6.4</strong>')
'''
y=['<strong>6.4</strong>','<strong>6.5</strong>','<strong>6.94</strong>']
x=[]
q=[]
class MYHTMLParser(HTMLParser):
    def handle_data(self, data):
        x.append(data)

parser=MYHTMLParser()
for item in ratings:
    parser.feed(str(item))
print(x)
