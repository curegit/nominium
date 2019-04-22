<?php
// データベースファイルへのパス
define("DB_PATH", realpath(__DIR__."/../../app/ziraffem.db"));

// データベースへの接続オブジェクトを返す
function open_db()
{
	// PDOで開く
	$pdo = new PDO("sqlite:".DB_PATH);
	// SQLクエリ実行時に例外を投げるようにする
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	// デフォルトフェッチを連想配列にする
	$pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
	// プリペアドステートメントのエミュレーションを無効化
	$pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	// PDOオブジェクトを返す
	return $pdo;
}
