
import requests
from bs4 import BeautifulSoup

source=requests.get("https://coreyms.com/page/5").text
soup=BeautifulSoup(source,"lxml")

for article in soup.find_all("article"):

    print()
    headline=article.h2.a.text
    print(headline)

    summary=article.find("div",class_="entry-content").p.text
    print(summary)



    try:
        video = article.find("iframe", class_="youtube-player")["src"]

        vid_id = video.split("/")[4].split("?")[0]

        yt_link = f"https://youtube.com/watch?v={vid_id}"

    except Exception as e:
        yt_link=None
    print(yt_link)
