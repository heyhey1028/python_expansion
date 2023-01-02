# Python Expansion Course

## 1. 環境構築
### Jupyter notebookの使い方
- pyenvをインストール
- pyenvを使ってanacondaを起動
```bash
$ pyenv shell anaconda3-4.2.0
```
- anacondaでjupyter notebookを起動
```bash
$ jupyter notebook
```
- localhost:8888でjupyter notebookがブラウザで起動される

## 2. python記法
1. {}の代わりにインデントでブロックを表現
2. if <条件>: , elif <条件>:, else:
3. 条件は`and`, `or`
4. `break`の代わりに`pass`を使う
5. ２単語以上の変数名では_(アンスコ)を使う ex. `my_name`
6. 変数の型チェックは`type()`メソッドを使う

## 3. データ型 List, Dictionary, Set, Tuple
### List
定義：`[]`で定義
```python
users = [
    "Tom", "John","Lisa"
]
```

Indexアクセス：
```python


```

## 4. スクレイピング
### HTMLサイトのスクレイピング
スクレイピングのステップは以下の通り
1. HTMLをサーバーから取得する
2. BeautifulSoupでHTMLを読み込む
3. DOMから情報を取り出す

```bash
$ pip3 install --upgrade beautifulsoup4
```

スクレイピングサンプル
```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pprint import pprint

# 1. Get HTML
with urlopen("http://www.yoheim.net") as res:
    html = res.read().decode("utf-8")

# 2. Load HTML with beautifulSoup
soup = BeautifulSoup(html, "html.parser")

# 3. Get items 
titles = soup.select(".articleListItem h2")
titles = [t.string for t in titles]

# 4. read scraped data
pprint(titles[:4])
```
- `res.read()`とする事で受け取ったhtmlをバイナリに変換する
- `.decode("utf-8")`でバイナリを更にutf-8に変換している
- `pretty print(pprint)`でリストを綺麗に整形してコンソール出力する

ステップ３でどのDOMにアクセスするかはサイトに応じて工夫する必要がある。その為、事前にスクレイピングを行いたいサイトをchromeなどのデベロッパツールを使って分析し、取得したいDOMを特定する必要がある。

デベロッパツールの矢印やコンソールを駆使して、どのようにアクセスすれば目当ての情報が取得出来るか確認する。

### BeautifulSoup

要素の選択
- select：CSSのセレクターを渡す事でDOMにアクセス。柔軟にアクセスする事が出来る為、大体`select`で選択可能。
- find：該当する要素を１つだけ取得。
- find_all

```python
# select
soup.select(".articleListItem h2")

# find
soup.find("h1")
soup.find(id="header_subtitle")
soup.find(class_="articleListItem")

# find_all
soup.find_all("h2")
soup.find(id="header_subtitle")
soup.find(class_="pubDate")
```

要素の取得
- text：DOM要素の文字列の取得
- attribute：htmlの属性の中身を取得。属性を引数に指定する。

```python
# <h1>My Special App</h1>
elm.string  # => My Special Appを取得

# <img src="/my_secret.png"/>
elm["src"]
```

### 標準出入力
スクレイピングの結果をファイルに出入力する事が多いので、扱いを知っておく

```python
# Read
f = open("my.txt")
txt = f.read()
f.close()

# Write
f = open("my2.txt", "w")
f.write("write something")
f.close()

# Read as Binary data
f = open("my.txt", "rb")
txt = f.read().decode("utf-8")
f.close()

# Auto Resourcing
with open("my.txt", "r") as f:
    txt = f.read()

```
- `rb`(read binary)で開く事でバイナリデータとして開く事が出来る
- バイナリデータの読み書きは画像データの読み込などで用いる事が多い
- `with`句を使う事でファイルのstreamを取得する事が出来る
- その為、`with`句を出ると`close()`を明示しなくてもファイルが自動的に閉じる

### Javascriptを使ってレンダリングしているサイトのスクレイピング



## 5. Webサーバー
### Flask
- request/response周りの機能が中心

インストール：
```
$ pip3 install --upgrade Flask
```

Flaskサーバーの起動：
```python
from flask import Flask
app = Flask(__name__)

@app.route("/") # サーバーのルーティング
def index():
    return "Hello from Flask"

if __name__ == "__main__": # Pythonコマンドから直接実行された時のみ実行される処理
    app.run()
```

- pythonコマンドから直接実行された場合は`__name__`が自動的に`__main__`となる為、`if __name__ == "__main__":`の条件式を用意する事でPythonコマンドのから直接実行された時(ex. 下記)の処理を記述する事が出来る
```bash
$ python3 app.py
```

ルーティング：
デコレーター(`@app.route`)を使う
```python
@app.route("/") 
def index():
    return "Hello from Flask"

@app.route("/api/hello")
def api_hello():
    return "Api hello"

@app.route("/api/items/<int:item_id>")
def api2(item_id):
    return "item_id is %d" % item_id
```

GETとPOST

```python
@app.route("/api/users", methods=["GET"])
def api_users_get():
    user_id = request.args.get("user_id")
    return "user_id is %s" % user_id

@app.route("/api/users/<int:user_id>", methods=["POST"])
def api_users_update(user_id):
    user_name = request.form.get("user_name")
    return "user_id=%d, user_name=%s" % (user_id,user_name)
```
- エンドポイントがどのhttpメソッドに反応するかはデコレーター内の第二引数methodsで複数指定することができる
- GET通信の場合は`request.args.get`でGETパラメータを展開する事が出来る
- POST通信のPOSTパラメータは`request.form.get`で展開する事が出来る

### Case1: Cookieを扱うrequest、response
#### Cookieの生成
```python
from datetime import datetime
from flask import Flask, make_response

@app.route("/cookie")
def cookie():
    # Contents
    response = make_response("OK") # レスポンスを生成
    # Create Cookie
    max_age = 60 * 60 * 24 * 30 # 30 days
    expires = int(datetime.now().timestamp()) + max_age
    response.set_cookie("gscookie", value = "hogehoge", expires=expires)
    # Response
    return response
```
- `make_response()`メソッドでレスポンスを生成する事が出来る
- `make_response()`の引数はクライアント側に返す文字列
- 生成したresponseクラスに対して`set_cookie()`メソッドでcookieを設置
- 第一引数にcookie名、その他valueパラメータに渡したい値やexpiresパラメータに有効期限を設定する事が可能

#### Cookieの取得
```python
from flask import Flask, request

@aap.route("/get_from_cookie")
def get_from_cookie():
    val = request.cookies.get("gscookie")
    return val
```
- `request.cookie.get()`でcookie名を指定し取得する

### Case2: Session
#### Sessionの取得

```python
from flask import Flask, session

app.secret_key = 'my_secret_key'

@app.route("/session")
def session_sample():
    val = int(session.get("num",1)) 
    session["num"] = val + 1
    return "%d回目の訪問ですね！" % val

```
- `app.secret_key`にてsessionの値を暗号化するキーを指定する必要がある
- `session.get()`で取得。第一引数にkey値を指定、第二引数では第一引数が取得できなかった場合のデフォルト値を指定
- sessionはdictionary型の為、`session["num]`の様に値にアクセスする


### Case3: アプリケーションの分割

### Case4: Logging

アプリケーションの定義


