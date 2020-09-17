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

初期プラグインの動作には以下が必要

- Requests (Python)
- Beautiful Soup 4 (Python)

### その他

- パスワードでログインできる SMTP サーバー（SSL 必須）

## インストール

1. すべてのファイルをサーバーに配置する
2. `conf/settings.ini` を書き換える
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

