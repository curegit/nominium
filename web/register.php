<?php
// 認証
require_once "./auth.php";
// インポート
require_once "./modules/html.php";
require_once "./modules/database.php";
// エラーメッセージなし
$error = "";
// エラー検証
try {
	// DB接続
	$pdo = open_db();
	// 登録
	$keyword = (string)filter_var($_POST["keyword"] ?? "");
	$importance = (float)filter_var($_POST["importance"] ?? 0, FILTER_VALIDATE_FLOAT);
	if ($keyword && $importance > 0 && $importance <= 1) {
		$stmt = $pdo->prepare("INSERT INTO keyword(keyword,importance) VALUES(?,?)");
		$stmt->bindValue(1, $keyword);
		$stmt->bindValue(2, $importance);
		$stmt->execute();
	}
	// 一覧取得
	$stmt = $pdo->query("SELECT * FROM keyword");
	$keywords = $stmt->fetchAll();
// エラー時
} catch (PDOException $e) {
	$error = $e->getMessage();
}
// ページ変数
define("PAGE_TITLE", "Register");
?>
<?php include "./frames/header.php"; ?>
<?php IF($error): ?>
    <section>
      <h2>Error</h2>
      <p><?= h($error) ?></p>
    </section>
<?php ELSE: ?>
<?php IF($keyword): ?>
    <section>
      <h2>Result</h2>
      <p>Registered: <?= h($keyword) ?></p>
    </section>
<?php ENDIF; ?>
    <section>
      <h2>Register</h2>
      <p>Register a new keyword</p>
      <form method="post">
        <label>Keyword: <input type="text" name="keyword"></label>
        <label>Importance: <input type="number" name="importance" min=0.01 max=1.0 step=0.01 value=0.8></label>
        <input type="submit" value="Register">
      </form>
    </section>
    <section>
      <h2>Registered Keywords</h2>
      <ul>
<?php FOREACH($keywords as $keyword_record): ?>
        <li><?= h($keyword_record["keyword"]) ?> [<?= h($keyword_record["importance"]) ?>] (Crawled <?= h($keyword_record["count"]) ?> times)</li>
<?php ENDFOREACH; ?>
      </ul>
    </section>
<?php ENDIF; ?>
<?php include "./frames/footer.php"; ?>
