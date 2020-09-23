<?php
$ini_path = realpath(__DIR__."/../../conf/settings.ini");
$ini_array = parse_ini_file($ini_path, true, INI_SCANNER_RAW);
$user = $ini_array["web"]["user"];
$password = $ini_array["web"]["password"];
switch (true) {
  case !isset($_SERVER["PHP_AUTH_USER"], $_SERVER["PHP_AUTH_PW"]):
  case $_SERVER["PHP_AUTH_USER"] !== $user:
  case $_SERVER["PHP_AUTH_PW"] !== $password:
    header("WWW-Authenticate: Basic realm=\"Nominium Web へのアクセス\"");
    header("Content-Type: text/plain; charset=utf-8");
    die("ログインしてください。".PHP_EOL);
}
