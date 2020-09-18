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
        <a class="item" href="<?= h($item["url"]) ?>">
          <div class="frame">
            <img class="image" src="<?= h($item["img"]) ?>">
            <div class="price">¥<?= h(number_format($item["price"])) ?></div>
          </div>
          <div class="title"><?= h($item["title"]) ?></div>
        </a>
<?php ENDFOREACH; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
