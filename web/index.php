<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $stmt = $pdo->query("SELECT * FROM keyword");
  $keywords = $stmt->fetchAll();
  $stmt = $pdo->query("SELECT * FROM item ORDER BY added DESC LIMIT 168");
  $items = $stmt->fetchAll();
  $error = "";
} catch (PDOException $e) {
  $error = $e->getMessage();
}

define("PAGE_TITLE", "ホーム");
?>
<?php include "./frames/header.php"; ?>
    <p>Nominium</p>
    <section>
      <h2>General</h2>
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
          <img src="<?= h($item["img"]) ?>" style="width: 200px; height: 200px;">
          <div><?= h($item["title"]) ?></div>
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
<?php ENDIF; ?>
<?php include "./frames/footer.php"; ?>
