# Nominium

個人間取引サイトの新着商品をメールなどで通知するクローラーシステム

<img src="web/assets/ziraffe.png" width="80px" height="80px">

## 設計概要

欲しい商品のコマースサイトでの入荷及び売り出しを、素早く検知することが目的のシステムです。

PHP による WEB ページインターフェースからデータベースに検索キーワードを登録すると、常駐する Python スクリプトによって定義済みコマースサイトにおけるクロールが反復的に実施されます。
新着アイテムが見つかれば、メールおよびその他の方法で通知を送信します。
クロール結果は WEB ページインターフェースでも確認できます。

## 動作要件

### 本体

- Linux システム
  - 推奨: Debian
- Apache 2
  - ディレクトリ毎の `.htaccess` が有効であること（使用できない場合は同等の設定を手動で行う）
  - nginx でも動作可（ただし、ディレクトリ毎 `.htaccess` のコンバートが必要）
- PHP 7.0 以上
  - SQLite3 (PDO) のサポート
  - `shell_exec` 関数のサポート
- Python 3.8 以上
  - Selenium 4 系
  - WebDriver (Firefox または Chrome または Chromium)
  - Webdriver Manager（オプション）
  - WebDriver はバイナリを手動指定するほか、Webdriver Manager, Selenium Manager による自動取得も利用可能
- パスワードでログインできる SMTP サーバー（標準の通知方法、要 SSL）

### プラグイン

同梱プラグインの動作には以下が追加で必要です。

- Requests (Python)
- Beautiful Soup 4 (Python)

## インストール手順

1. すべてのファイルをサーバーに配置する
2. 設定テンプレート `conf/settings.sample.ini` から、設定ファイル `conf/settings.ini` を作成
3. 設定ファイル `conf/settings.ini` を書き換える
4. `app/setup.py` を Python インタプリタで実行する
5. `app/test.py` を Python インタプリタで実行し、Selenium とメール送信の動作を確認する

## 使い方

ブラウザで `web/` を訪問し（初期パスワードは設定ファイルを参照）、検索キーワードを登録します。
その後、Python インタプリタで `app/nominium.py <稼働時間（秒）>` を実行すると、指定された稼働時間だけプログラムが走り続け、実行されている間の新着商品がメールで通知されます。
通知を永続的に受け取るには、なんらかの方法（例えば、cron などのジョブスケジューラーを使う）でこのプログラムが恒常的に実行されるようにしてください。
クロールするサイトとその手続きはプラグインの形で定義されます。

`app/nominium.py` は割り込みシグナル (SIGINT) で終了 (Graceful Shutdown) できます。
シャットダウンシグナル (SIGTERM) で急速終了できます。

## プラグイン

各プラグインは `app/plugins/enabled.py` にモジュールを追加することで有効化されます。

### サイト

クロールするサイトとその方法を定義します。
モジュールには以下 3 つの値を定義する必要があります。

- `name`: サイト名文字列、他サイトとの区別に使用
- `get(driver, keyword)`: 文字列 `keyword` のクロール結果を返す関数、`driver` は任意で利用できる Selenium WebDriver インスタンス
- `extract(documents)`: `get` の戻り値からアイテム情報（複数）を抽出する関数

`extract` の戻り値はタプル `(id, url, title, img, thumbnail, price)` のイテレーターである必要があります。
`price` のみ `int` 型です。

- `id`: そのサイトでの固有アイテム ID
- `url`: そのアイテムの URL
- `title`: アイテムの名前
- `img`: アイテムの画像リソース URL
- `thumbnail`: アイテムの画像（小さいサイズ）リソース URL
- `price`: 価格（円）

オプションで以下 2 つの値を追加定義できます。

- `query(keyword)`: 検索 URL を生成する関数
- `queryjs`: 検索 URL を生成する JavaScript 関数の文字列

`queryjs` は WEB ページインターフェースで使用されます。

### 通知

任意の通知動作を定義できます。
`app/plugins/hooks/skeleton.py` を利用して作成してください。

## クリーニング

`app/clean.py` を Python インタプリタで実行すると、ログファイルとデータベース中のクロールデータが削除されます。
登録しているキーワードなどは削除されません。

## データの初期化

`app/setup.py` を Python インタプリタで再実行すると、ログファイルとデータベース中の全データが削除されます。
登録しているキーワードなども削除されます。
設定ファイルは変更されません。

## 設定ファイル

### `general` セクション

プログラムの基本動作を設定します。

| 項目                | 値の形式   | 説明                                                               |
| ------------------- | ---------- | ------------------------------------------------------------------ |
| `wait`              | 自然数     | 1 つのフェッチャーが 1 回のダウンロードごとに定常的に待つ秒数      |
| `max_rate`          | 自然数     | 1 つのフェッチャーが 1 回のダウンロードにかける最低秒数            |
| `patience`          | 正整数     | `patience` 回数失敗したクエリを失敗上限に達したとみなす            |
| `backoff`           | 自然数     | 失敗上限を超えたクエリを `backoff` 秒間再試行しない                |
| `cut`               | 正整数     | 既知のアイテムがこの数連続で出現したら抽出を打ち切る               |
| `enough`            | 正整数     | ダウンロードしたページから抽出する十分なアイテムの数               |
| `parallel`          | 正整数     | この数のフェッチャーを並列で起動してダウンロードする               |
| `max_price`         | 自然数     | この価格以下なら通知する                                           |
| `max_notify_hourly` | 自然数     | 1 時間で送信する最大の通知数                                       |
| `while_stopped`     | 0 または 1 | 1 ならばプログラム停止中の新着アイテムも次回起動時の通知対象とする |

### `selenium` セクション

Selenium 起動のためのオプション群です。

`browser` フィールドで Selenium が使うブラウザを指定します。
Firefox, Chrome, Chromium のいずれかです。

`wdm` が 1 のとき、Webdriver Manager によって、対応する WebDriver が自動取得（さらにキャッシュ）されます。
`wdm` が 0 のときは、`driver` フィールドに、使用する WebDriver のパスを記述してください。
`driver` フィールドが空のときは、Selenium Manager による自動取得が行われます。

`headless` が 0 だと通常の GUI モード、1 だと headless モードで起動します。
CUI 環境では 1 にセットする必要があります。

`timeout` で Webdriver がページロードを待つ最大秒を設定できます。

### `smtp` セクション

メール送信に使用する情報を記入します。
`enabled` を 0 にするとメール通知を無効化します。
`to` フィールドはカンマ区切りで複数指定ができます。

### `web` セクション

組み込みの Basic 認証についての設定です。
Web インターフェイスにログインするための情報を記入します。
このセクションのみ、値に英数字ではないものがある場合はダブルクォートで囲む必要があります（PHP モジュールの仕様による）。

`auth` が 1 のときは、組み込みの Basic 認証が有効になるので、`user` と `password` の組み合わせでログインをします。
`auth` を 0 にすると、組み込みの Basic 認証が無効になります。
システムがプライベートネットワークにあるため認証が不要な場合や、WEB サーバープログラムの認証機能を利用する場合などにおいて、そのように設定します。

## 注意事項

- SSL 証明書を検証しないなどの望ましくない振る舞いを含んでいます。
- 設定ファイルはパスワードを平文で保持するので扱いに注意してください。

## ライセンス

[CC BY-NC 4.0](LICENSE)
