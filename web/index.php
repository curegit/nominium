<?php
// 認証
require_once "./auth.php";
// インポート
require_once "./modules/manifest.php";
require_once "./modules/html.php";
require_once "./modules/logging.php";
require_once "./modules/database.php";
// エラーメッセージなし
$error = "";
// エラー検証
try {
	// キーワード一覧取得
	$pdo = open_db();
	$stmt = $pdo->query("SELECT * FROM keyword");
	$keywords = $stmt->fetchAll();
	// 最近の商品を取得
	$stmt = $pdo->query("SELECT * FROM item ORDER BY added DESC LIMIT 56");
	$items = $stmt->fetchAll();
// エラー時
} catch (PDOException $e) {
	$error = $e->getMessage();
}
// ページ変数
define("PAGE_TITLE", "Home");
?>
<?php include "./frames/header.php"; ?>
    <p><?= h(APP_ABBREVIATION) ?> works for you!</p>
    <section>
      <h2>General</h2>
      <p>
        Name: <?= h(APP_NAME) ?> (<?= h(APP_ABBREVIATION) ?>)<br>
        Version: <?= h(VERSION) ?><br>
        DB: <?= h(DB_PATH) ?><br>
        Logs: <?= h(LOG_DIR) ?>
      </p>
    </section>
<?php IF($error): ?>
    <section>
      <h2>Error</h2>
      <p><?= h($error) ?></p>
    </section>
<?php ELSE: ?>
    <section>
      <h2>Recent Items</h2>
<?php FOREACH($items as $item): ?>
      <a href="<?= h($item["url"]) ?>">
        <div style="width: 200px; height: 260px; float: left; margin: 10px; overflow: hidden;">
          <img src="<?= h($item["img_url"]) ?>" style="width: 200px; height: 200px;">
          <div><?= h($item["name"]) ?></div>
        </div>
      </a>
<?php ENDFOREACH; ?>
    </section>
    <section style="clear: both;">
      <h2>Registered Keywords</h2>
      <ul>
<?php FOREACH($keywords as $keyword_record): ?>
        <li><?= h($keyword_record["keyword"]) ?></li>
<?php ENDFOREACH; ?>
      </ul>
    </section>
    <section>
      <h2>Today Logs</h2>
      <pre><?= h(get_today_logs()) ?></pre>
    </section>
<?php ENDIF; ?>
<?php include "./frames/footer.php"; ?>
