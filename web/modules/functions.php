<?php
// HTMLメタ文字のエスケープ
function h($str) {
  return htmlspecialchars($str, ENT_QUOTES, "UTF-8");
}

// インラインスクリプトに安全な文字列かどうか
function is_safe_for_inline_script($str) {
  $match = preg_match("/<\/script(\/| |>)/i", $str);
  if ($match === false) {
    return false;
  }
  return $match ? false : true;
}

// リクエスト中に変わらないノンスを生成
function nonce() {
  static $cache = null;
  if ($cache === null) {
    $cache = hash("sha256", random_bytes(1024));
  }
  return $cache;
}

// サイトごとのクエリの組み立て方を返す
function queries() {
  static $cache = null;
  if ($cache === null) {
    $json_path = realpath(__DIR__."/../../data/queries.json");
    $res = file_get_contents($json_path);
    if ($res === false) {
      $cache = json_decode("{}", true);
    } else {
      $cache = json_decode($res, true);
    }
  }
  return $cache;
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
    $log_path_arg = escapeshellarg($log_path);
    return `tail -n $n $log_path_arg`;
  } else {
    return false;
  }
}

// 実行中のメインアプリPID等を返す
function get_running_status() {
  $json_file = realpath(__DIR__."/../../data/process.json");
  if (!file_exists($json_file) || filesize($json_file) <= 0) {
    return false;
  }
  $res = file_get_contents($json_file);
  if ($res === false) {
    return false;
  }
  $json_data = json_decode($res, true);
  if (!$json_data) {
    return false;
  }
  $pid = $json_data["pid"];
  $start_time = $json_data["start_time"];
  $end_time = $json_data["end_time"];
  $current_start_time = get_process_start_time($pid);
  if ($current_start_time === $start_time) {
    return array("pid" => $pid, "start" => $start_time, "end" => $end_time);
  }
  return false;
}

// プロセスの開始時刻を取得
function get_process_start_time($pid) {
  $pid_arg = escapeshellarg($pid);
  $output = `ps -o lstart= -p $pid_arg`;
  if (!$output) {
    // プロセスが存在しない
    return false;
  }
  // UNIX timestampに変換
  return strtotime(trim($output));
}
