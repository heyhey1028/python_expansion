import os
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://dokusho-ojikan.jp/ranking/daily/1?ref=global_navigation_ranking")

html= driver.page_source

# Get image urls
bs = BeautifulSoup(html, "html.parser")
img_urls = [img.get("src") for img in bs.find_all("img", limit=10)]

# Convert file name

# Create directory
if not os.path.exists("img2"):
    os.mkdir("img2")

# Create img file 
for i, url in enumerate(img_urls):
    print(i, url)
    with urlopen(url) as res:
        img = res.read()
        with open("img2/%d.png" % (i+1),"wb") as f:
            f.write(img)

# Screenshot
driver.save_screenshot("ss.png")

driver.quit()