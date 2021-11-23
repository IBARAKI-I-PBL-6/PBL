# 茨城高専4年情報系PBL実験6班

## 環境構築の方法

1. python3.10をインストールする

   [このページ](https://www.python.org/downloads/release/python-3100/) からダウンロードできます。

2. pipenvをインストールする

   `py -3.10 -m pip install pipenv`でインストールできます。(高専WiFiではプロキシを設定しないとうまくいかないので注意!)

3. パッケージを更新する

   `pipenv update`でパッケージを一斉に更新できます。

### 環境構築に関するFAQ

Q1. **ファイルを実行するときはどうすればいいの?**

A1. `pipenv run python (実行したいファイル名)`でできます

(しかもバージョンは勝手に3.10.0になるから便利!)

Q2. パッケージをインストールするにはどうすればいいの?

A2. `pipenv install (インストールしたいモジュール名)`でできます

そうすることで、ファイルの実行時に(インストールしたいモジュール名を手元でインストールしていなくても)勝手にインストールしてくれます。

## loggingについて

loggingとは、実行中にでたログなどをファイルや標準エラー出力に出力するためのモジュールです。

ログのレベルは小さい順に`notset`,`debug`,`info`,`warning`,`error`,`critical`となっており、ここでは、debug以上がファイルに、info以上が標準エラー出力に出力されます。
また、ログファイルは`log/root.log`に保存され、深夜を過ぎると、その分の内容が`log/root.log.(日付)`に移動されます。

参考:[リファレンス情報](https://docs.python.org/ja/3/library/logging.html), [チュートリアル](https://docs.python.org/ja/3/howto/logging.html#logging-basic-tutorial)

### loggingの使い方

- ログを出力するファイルの処理
  
  先頭に、次の2行を入れてください。

```text
from logging import getLogger
logger = getLogger(__name__)
```

  その後、`logger.info(メッセージ)`などとすることでログを出すことができます。

- プログラムを実行するファイルの処理
  
  先頭に、つぎの2行を追加してください。

```py
from src.logging_setting import set_logger
set_logger()
```

  その時に、別のファイルから呼びされるときに`set_logger()`が呼び出されないように注意してください。

  (実行用の関数は`if __name__ == "main":`から始めることを推奨します)

## pytestについて

pytestとは、単体テストを書くためのフレームワークの一つです。

### テストの書き方

まず、`src/tests`に`test_(任意の名前).py`というファイルを追加してください。
そのファイルにテストしたいモジュールを`pytest`をインポートしてください。

そして、そのファイルに`test_`から始まる関数を作成してください。

`assert (想定する結果が真になる条件)`で関数をテストすることができます。

(ここで書いた内容は最低限のものなので、詳細は <https://rinatz.github.io/python-book/ch08-02-pytest/> を見てください。)

### テストの実行の仕方

はじめに、`pipenv show pytest`で`pytest`がインストールされているか確認してください。

(インストールされていない場合は`pipenv update`でインストールできます)

そして、`pipenv run pytest`でテストを実行することができます。

## ブランチに関するお願い

開発したコードはまずはmain以外のブランチでプッシュしてください。

そのあとに、mainにプルリクエストをお願いします。
