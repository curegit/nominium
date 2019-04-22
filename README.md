# Ziraffe Roams Markets

## 要件

- PHP7 + sqlite(PDO)
- Python3
- Selenium(Python) + WebDriver

## インストール

- app/settings.ini を書き換える
- app/setup.py を実行
- web/settings/password.php を書き換える
- /web/ にブラウザでアクセスしてキーワードを登録
- app/ziraffem.py を定期実行するように登録する

### 稼働時間

settings.ini の time 秒実行される。time を 64800 として朝7時に起動すると25時に終了する。

### crontab の例

```
0 7 * * * python3 /home/username/public_html/ziraffem/app/ziraffem.py
```

## Selenium のテスト

app/seletest.py を実行

## メール送信テスト

app/mailtest.py を実行
