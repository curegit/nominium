# Ziraffe Roams Markets

メルカリとラクマの新着商品をメールで通知するクローラー

## 動作条件

### Raspbian の場合

- PHP 7 + SQLite (PDO)
- Python 3 + Selenium (Python) + WebDriver (Chromium)

## インストール

1. すべてのファイルをサーバーに配置する
2. `app/settings.ini` を書き換える
3. `app/setup.py` を実行
4. `web/settings/password.php` を書き換える
5. ブラウザで `/web/` へ行って検索キーワードを登録
6. `app/ziraffem.py` が毎日実行されるようにする

### 稼働時間

`app/ziraffem.py` の稼働時間は `settings.ini` の `time` で制御する。
例えば、64800 に設定して午前7時に起動すると、午前1時に終了する。

### Crontab の例

毎朝7時に起動する例

```
0 7 * * * python3 /home/username/public_html/ziraffem/app/ziraffem.py
```

## 動作確認

### Selenium

`app/seletest.py` を実行

### メール送信

`app/mailtest.py` を実行
