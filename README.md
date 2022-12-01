# Nominium

個人間取引サイトの新着商品をメールなどで通知するクローラー

<img src="web/assets/ziraffe.png" width="80px" height="80px">

## 動作要件

### 本体

- Linux システム
  - `tail` コマンド
- Apache 2
  - `mod_rewrite` モジュール
  - ディレクトリ毎の `.htaccess` が有効であること
  - Nginx で代替可（ただし、ディレクトリ毎 `.htaccess` のコンバートが必要）
- PHP 7.0 以上
  - SQLite (PDO) のサポート
  - `shell_exec` 関数のサポート
- Python 3.6 以上
  - Selenium 4
  - WebDriver (Firefox または Chrome または Chromium)
  - Webdriver Manager（オプション）
  - WebDriver はバイナリを手動指定するほか、Webdriver Manager による自動取得も利用可能
- パスワードでログインできる SMTP サーバー（要 SSL）

### プラグイン

初期プラグインの動作には以下が必要です。

- Requests (Python)
- Beautiful Soup 4 (Python)

## インストール手順

1. すべてのファイルをサーバーに配置する
2. 設定ファイル `conf/settings.ini` を書き換える
3. `app/setup.py` を Python インタプリタで実行する
4. `app/test.py` を Python インタプリタで実行し、Selenium とメール送信の動作を確認する

## 使い方

ブラウザで `web/` を訪問し（初期パスワードは設定ファイルを参照）、検索キーワードを登録します。
その後、Python インタプリタで `app/nominium.py <稼働時間（秒）>` を実行すると、指定された稼働時間だけプログラムが走り続け、実行されている間の新着商品がメールで通知されます。
通知を永続的に受け取るには、なんらかの方法（例えば、cron などのジョブスケジューラーを使う）でこのプログラムが恒常的に実行されるようにしてください。
クロールするサイトとその手続きはプラグインの形で定義されます。

## プラグイン

各プラグインは `app/plugins/enabled.py` にモジュールを追加することで有効化されます。

### サイト

クロールするサイトとその方法を定義します。
モジュールには以下 3 つの値を定義する必要があります。

- name: サイト名、他サイトとの区別に使用
- get(driver, keyword): クロール結果を返します
- extract(documents): get の戻り値からアイテム情報を抽出します

extract の戻り値は以下のタプルである必要があります。
id, url, title, img, thumbnail, price

### 通知

任意の通知動作を定義できます。
`app/plugins/hooks/skeleton.py` を利用して作成してください。

## クリーニング

`app/clean.py` を Python インタプリタで実行すると、ログファイルとデータベース中のクロールデータが削除されます。
登録しているキーワードなどは削除されません。

## データの初期化

`app/setup.py` を Python インタプリタで再実行すると、ログファイルとデータベース中の全データが削除されます。
設定ファイルは変更されません。

## 設定ファイル

### `general` セクション

プログラムの基本動作を設定します。

| 項目                | 値の形式   | 説明                                                               |
|---------------------|------------|--------------------------------------------------------------------|
| `wait`              | 自然数     | 1 つのフェッチャーが 1 回のダウンロードごとに定常的に待つ秒数      |
| `max_rate`          | 自然数     | 1 つのフェッチャーが 1 回のダウンロードにかける最低秒数            |
| `patience`          | 正整数     | `patience` 回数失敗したクエリを失敗上限に達したとみなす            |
| `backoff`           | 自然数     | 失敗上限を超えたクエリを `backoff` 分間再試行しない                |
| `cut`               | 正整数     | 既知のアイテムがこの数連続で出現したら抽出を打ち切る               |
| `enough`            | 正整数     | ダウンロードしたページから抽出する十分なアイテムの数               |
| `parallel`          | 正整数     | この数のフェッチャーを並列で起動してダウンロードする               |
| `max_price`         | 自然数     | この価格以下なら通知する                                           |
| `max_notify_hourly` | 自然数     | 1 時間で送信する最大の通知数                                       |
| `while_stopped`     | 0 または 1 | 1 ならばプログラム停止中の新着アイテムも次回起動時の通知対象とする |

### `selenium` セクション

Selenium 起動のためのオプション群です。
`driver` フィールドに ChromeDriver のパスを記述してください。

### `smtp` セクション

メール送信に使用する情報を記入します。
`enabled` を 0 にするとメール通知を無効化します。

### `web` セクション

Web インターフェイスにログインするための情報を記入します。
このセクションのみ、値に英数字ではないものがある場合はダブルクォートで囲む必要があります（PHP モジュールの仕様による）。

## サービス化

## 注意事項

- SSL 証明書を検証しないなどの望ましくない振る舞いを含んでいます。
- 設定ファイルはパスワードを平文で保持するので扱いに注意してください。

## ライセンス

[CC BY-NC 4.0](LICENSE)
