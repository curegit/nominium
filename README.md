<img alt="Ziraffe" src="web/assets/ziraffe.png" width=80 height=80>

# Ziraffe Roams Markets

A crawler of some c2c e-commerce sites to buy what you want faster than anybody else

## Requirements

### Raspbian

- PHP7 + sqlite(PDO)
- Python3 + Selenium(Python) + WebDriver(Chromium)

## Installation

1. Deploy all files to a server
2. Rewrite `app/settings.ini`
3. Execute `app/setup.py`
4. Rewrite `web/settings/password.php`
5. Go to `/web/` via browser, and register keywords
6. Make `app/ziraffem.py` run continuously

### Running Time

The crawler keeps running for `time` seconds written in `settings.ini` every execution.
For example, if `time` is set to 64800, it finishes at 1 a.m. when it is executed at 7 a.m.

### Crontab Instance

Common one that it wake up at 7 everyday

```
0 7 * * * python3 /home/username/public_html/ziraffem/app/ziraffem.py
```

## Tests

### Selenium

Run `app/seletest.py`

### Mail

Run `app/mailtest.py`
