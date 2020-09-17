<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $stmt = $pdo->query("SELECT * FROM item ORDER BY added DESC LIMIT 168");
  $items = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  $error = $e->getMessage();
}

define("PAGE_TITLE", "ホーム");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($error): ?>
      <section>
        <h2>エラー</h2>
        <p><?= h($error) ?></p>
      </section>
<?php ELSE: ?>
      <section class="items">
<?php FOREACH($items as $item): ?>
        <a href="<?= h($item["url"]) ?>">
          <img src="<?= h($item["img"]) ?>">
          <div><?= h($item["title"]) ?></div>
          <div>¥<?= h(number_format($item["price"])) ?></div>
        </a>
<?php ENDFOREACH; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
