import requests
from bs4 import BeautifulSoup

user_input=input("Please enter the genre: ")
source=requests.get("https://www.imdb.com/search/title/?genres="+ user_input).text
soup=BeautifulSoup(source,"lxml")

for article in soup.find_all("div", class_="lister-item-content")[0:5]:
    print()
    headline=article.h3.a.text
    summary=article.find_all("p",class_="text-muted")[1].text
    movie_launch=article.find("span",class_="lister-item-year text-muted unbold").text[1:5]
    movie_duration=article.find("span",class_="runtime").text
    movie_rating=article.find("div",class_="inline-block ratings-imdb-rating").text
    director=article.find_all("p")[2]("a")[0].text
    star1=article.find_all("p")[2]("a")[1].text
    star2=article.find_all("p")[2]("a")[2].text
    star3=article.find_all("p")[2]("a")[3].text



#cover=article.h3.a["href"]
#print(cover)

#poster="https://www.imdb.com/"+cover
#print(poster)

