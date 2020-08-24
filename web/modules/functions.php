<?php
// HTMLメタ文字のエスケープ
function h($html) {
  return htmlspecialchars($html, ENT_QUOTES, "UTF-8");
}

// データベースへの接続を開いて返す
function open_db() {
  $db_path = __DIR__."/../../app/ziraffem.db";
  $pdo = new PDO("sqlite:".$db_path);
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
  $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
  return $pdo;
}
