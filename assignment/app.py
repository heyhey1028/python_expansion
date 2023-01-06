import json
from urllib.request import urlopen
import random
from flask import Flask, render_template
from bs4 import BeautifulSoup
from pprint import pprint


app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    # 1. はてブのホットエントリーページのHTMLを取得する
    url = "https://b.hatena.ne.jp/hotentry/all"
    with urlopen(url) as res:
        html = res.read()
        
    # 2. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")

    # 3. 記事一覧を取得する
    articles = soup.select(".entrylist-contents-title a")
    
    # 4. ランダムに1件取得する
    article = random.choice(articles)

    # 5. json形式で返却する
    return json.dumps({
        "content" : article["title"],
        "link" : article["href"]
    })

@app.route("/api/tokyo_weather")
def api_tokyo_weather():
    url = "https://weather.yahoo.co.jp/weather/jp/13/4410.html"
    with urlopen(url) as res:
        html = res.read()

    soup = BeautifulSoup(html, "html.parser")

    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    return rs[0] + "の東京の天気は" + rs[1] + "、明日は" + rs[19] + "です。"

if __name__ == "__main__":
    app.run(debug=True, port=5004)
