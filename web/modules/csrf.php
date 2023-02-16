<?php
if ($_SERVER["REQUEST_METHOD"] !== "GET" && $_SERVER["REQUEST_METHOD"] !== "HEAD") {
  if (!isset($_SERVER["HTTP_SEC_FETCH_SITE"]) || strtolower($_SERVER["HTTP_SEC_FETCH_SITE"]) !== "same-origin") {
    http_response_code(400);
    header("Content-Type: text/plain; charset=utf-8");
    die("不正な遷移です。".PHP_EOL);
  }
}
