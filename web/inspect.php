<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

$n = 2000;
$log = get_today_log($n);

define("PAGE_TITLE", "監査");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($log === null): ?>
      <section>
        <h2>エラー</h2>
        <p>ログの読み取りに失敗しました。</p>
      </section>
<?php ELSE: ?>
      <section>
        <h2>今日のログ</h2>
<?php IF($log === false): ?>
        <p>今日のログはありません。</p>
<?php ELSE: ?>
        <p>最大で末尾から <?= h($n) ?> 行を表示します。</p>
        <pre class="log"><?= h($log) ?></pre>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
