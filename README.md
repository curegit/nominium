# Nominium

個人間取引サイトの新着商品をメールで通知するクローラー

## 動作環境

### 基本

- Apache 2
  - ディレクトリ毎の `.htaccess` が有効であること
- PHP 7 以上
  - Apache 2 で使用できること
  - SQLite (PDO)
- Python 3.6 以上
  - Selenium + WebDriver (Chrome または Chromium)

### プラグイン

初期プラグインの動作には以下が必要です。

- Requests (Python)
- Beautiful Soup 4 (Python)

### その他

- パスワードでログインできる SMTP サーバー（SSL 必須）

## インストール

1. すべてのファイルをサーバーに配置する
2. 設定ファイル `conf/settings.ini` を書き換える
3. `app/setup.py` を Python インタプリタで実行
4. `app/test.py` を Python インタプリタで実行し、Selenium とメール送信の動作を確認

## 使い方

ブラウザで `web/` へ行って検索キーワードを登録
`app/nominium.py` が毎日実行されるようにする

### 稼働時間

`app/ziraffem.py` の稼働時間は `settings.ini` の `time` で制御する。
例えば、64800 に設定して午前7時に起動すると、午前1時に終了する。

### Crontab の例

毎朝7時に起動する例

```
0 7 * * * python3 /home/username/public_html/ziraffem/app/ziraffem.py
```

## クリーニング

## 設定ファイル

### `general` セクション

|  項目  |  値の形式  | 説明 |
| ---- | ---- | ---- |
|  `wait`  |  自然数  |  |
|  `max_rate`  |  自然数  |  |
|  `cut`  |    |  |
|  `enough`  |  自然数  |  |
|  `parallel`  |  自然数  |  |
|  `max_price`  |    |  |
|  `max_notify_hourly`  |    |  |
|  `while_stopped`  |  0 または 1  |  |


wait = 3
max_rate = 8
cut = 10
enough = 50
parallel = 4
max_price = 100000
max_notify_hourly = 30
`while_stopped`

### `selenium` セクション

Selenium 起動のためのオプション群です。
`driver` に ChromeDriver のパスを記述してください。

### `smtp` セクション

メール送信に使用する情報を記入します。

### `web` セクション

Web インターフェイスにログインするための情報を記入します。
このセクションのみ、値に英数字ではないものがある場合はダブルクォートで囲む必要があります（PHP モジュールの仕様による）。

## 注意事項

- SSL 証明書を検証しないなどの望ましくない振る舞いを含んでいます。
- 設定ファイルはパスワードを平文で保持するので、扱いに注意してください。

## ライセンス
