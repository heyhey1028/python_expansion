import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""

    """
        **** ここを実装します（基礎課題） ****

        1. はてブのホットエントリーページのHTMLを取得する
        2. BeautifulSoupでHTMLを読み込む
        3. 記事一覧を取得する
        4. ランダムに1件取得する
        5. 以下の形式で返却する.
            {
                "content" : "記事のタイトル",
                "link" : "記事のURL"
            }
    """

    # ダミー
    return json.dumps({
        "content" : "記事のタイトルだよー",
        "link" : "記事のURLだよー"
    })

@app.route("/api/xxxx")
def api_xxxx():
    """
        **** ここを実装します（発展課題） ****
        ・自分の好きなサイトをWebスクレイピングして情報をフロントに返却します
        ・お天気APIなども良いかも
        ・関数名は適宜変更してください
    """
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5004)
