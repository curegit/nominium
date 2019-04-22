<?php
// ログディレクトリ
define("LOG_DIR", realpath(__DIR__."/../../app/logs"));

// 今日のログファイルのパスを返す
function log_filepath()
{
	$date = date("Y-m-d");
	return LOG_DIR."/{$date}.log";
}

// 今日のログファイルの内容を返す
function get_today_logs()
{
	$path = log_filepath();
	if (file_exists($path) && filesize($path) > 0) {
		return file_get_contents($path);
	} else {
		return "No logs yet today".PHP_EOL;
	}
}
