<?php
// HTMLメタ文字のエスケープ
function h($str) {
  return htmlspecialchars($str, ENT_QUOTES, "UTF-8");
}

// クエリの組み立て方 JSON を返す
function queries() {
  $json_path = realpath(__DIR__."/../../data/queries.json");
  $res = file_get_contents($json_path);
  if ($res === false) {
    return "{}";
  } else {
    return $res;
  }
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

// PDO例外が整合性制約違反なら真 (ANSI SQL-92)
function is_integrity_constraint_violation($error) {
  $code = (int)($error->getCode());
  return 23000 <= $code && $code < 24000;
}

// ログファイルの内容を返す
function get_recent_log($n, $error = false) {
  $name = $error ? date("Y-m")."-error" : date("Y-m-d");
  $log_path = realpath(__DIR__."/../../logs/{$name}.log");
  if (file_exists($log_path) && filesize($log_path) > 0) {
    return `tail -n $n $log_path`;
  } else {
    return false;
  }
}
