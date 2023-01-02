import os
from urllib.request import urlopen
from pprint import pprint
from bs4 import BeautifulSoup

# get html from server
with urlopen("http://gsacademy.jp/mentor-lecturer") as res:
    html = res.read().decode("utf-8")

# get BeautifulSoup Instance
soup = BeautifulSoup(html, "html.parser")

# create list of image's urls
img_urls = [e["src"] for e in soup.select(".mentor__list-item-img img")] # リスト内包表記

# convert 
img_urls = [u if u.find("http") == 0 else "http://gsacademy.jp" + u for u in img_urls]

# Create directory
if not os.path.exists("img"):
    os.mkdir("img")

# Create img file 
for i, url in enumerate(img_urls):
    print(i, url)
    with urlopen(url) as res:
        img = res.read()
        with open("img/%d.png" % (i+1),"wb") as f:
            f.write(img)
