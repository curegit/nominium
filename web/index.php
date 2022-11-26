<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $stmt = $pdo->query("SELECT * FROM item ORDER BY added DESC LIMIT 504");
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
      <script defer src="./assets/refresh.js"></script>
      <script defer src="./assets/filter.js"></script>
      <section>
        <div class="control">
          <div class="group">
            <label><input type="checkbox" id="auto-update-enabled" onchange="setschedule()">自動更新</label>
            <select name="auto-update" id="auto-update-interval" onchange="setschedule()">
              <option value="15">15 秒</option>
              <option value="30">30 秒</option>
              <option value="60" selected>1 分</option>
              <option value="180">3 分</option>
              <option value="300">5 分</option>
            </select>
          </div>
          <div class="group">
            <label>フィルタ</label>
            <select name="filter" id="filter-select" onchange="setfilter()">
              <option value="-1">すべてを表示</option>
              <option value="0" selected>通知対象のみ</option>
              <option value="1">稼働時間外による非通知対象</option>
              <option value="2">値段上限による非通知対象</option>
              <option value="3">フィルタによる非通知対象</option>
            </select>
          </div>
        </div>
        <h2>新着アイテム</h2>
<?php IF($items): ?>
        <div class="items">
<?php FOREACH($items as $item): ?>
          <article class="item notify<?= h($item["notify"]) ?>">
            <a href="<?= h($item["url"]) ?>">
              <div class="frame">
                <img class="image" src="<?= h($item["img"]) ?>">
                <div class="price">¥<?= h(number_format($item["price"])) ?></div>
              </div>
              <h3 class="title"><?= h($item["title"]) ?></h3>
            </a>
          </article>
<?php ENDFOREACH; ?>
        </div>
<?php ELSE: ?>
        <p class="nothing">まだ何もインデックスされていません。</p>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
