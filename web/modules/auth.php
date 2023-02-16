<?php
$ini_path = realpath(__DIR__."/../../conf/settings.ini");
$ini_array = parse_ini_file($ini_path, true, INI_SCANNER_RAW);
$auth = filter_var($ini_array["web"]["auth"], FILTER_VALIDATE_BOOLEAN);
if ($auth) {
  $user = $ini_array["web"]["user"];
  $password = $ini_array["web"]["password"];
  switch (true) {
    case !isset($_SERVER["PHP_AUTH_USER"], $_SERVER["PHP_AUTH_PW"]):
      http_response_code(401);
      header("Content-Type: text/plain; charset=utf-8");
      die("ログインしてください。".PHP_EOL);
    case $_SERVER["PHP_AUTH_USER"] !== $user:
    case $_SERVER["PHP_AUTH_PW"] !== $password:
      http_response_code(401);
      header("WWW-Authenticate: Basic realm=\"Nominium Web Interface\"");
      header("Content-Type: text/plain; charset=utf-8");
      die("認証に失敗しました。".PHP_EOL);
  }
}
