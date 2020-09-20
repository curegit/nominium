<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

$log = get_today_log();

define("PAGE_TITLE", "ログ");
?>
<?php include "./frames/header.php"; ?>
    <main>
      <section>
        <h2>ログ</h2>
<?php IF($log === false): ?>
        <p>今日のログがありません。</p>
<?php ELSE: ?>
        <p></p>
        <pre><?= h($log) ?></pre>
<?php ENDIF; ?>
      </section>
    </main>
<?php include "./frames/footer.php"; ?>
