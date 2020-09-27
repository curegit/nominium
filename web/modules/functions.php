<?php
// HTMLメタ文字のエスケープ
function h($str) {
  return htmlspecialchars($str, ENT_QUOTES, "UTF-8");
}

// データベースへの接続を開いて返す
function open_db() {
  $db_path = realpath(__DIR__."/../../data/nominium.db");
  $pdo = new PDO("sqlite:".$db_path);
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
  $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
  return $pdo;
}

// 今日のログファイルの内容を返す
function get_today_log($tail) {
  $date = date("Y-m-d");
  $log_path = realpath(__DIR__."/../../logs/{$date}.log");
  if (file_exists($log_path) && filesize($log_path) > 0) {
    return `tail -n $tail $log_path`;
  } else {
    return false;
  }
}
