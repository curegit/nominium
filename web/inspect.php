<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

$log = get_today_log();

define("PAGE_TITLE", "監査");
?>
<?php include "./frames/header.php"; ?>
    <main>
      <section>
        <h2>今日のログ</h2>
<?php IF($log === false): ?>
        <p>今日のログはありません。</p>
<?php ELSE: ?>
        <pre class="log"><?= h($log) ?></pre>
<?php ENDIF; ?>
      </section>
    </main>
<?php include "./frames/footer.php"; ?>
