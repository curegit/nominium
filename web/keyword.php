<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $stmt = $pdo->query("SELECT * FROM keyword ORDER BY priority DESC");
  $keywords = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  $error = $e->getMessage();
}

define("PAGE_TITLE", "キーワード");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($error): ?>
      <section>
        <h2>エラー</h2>
        <p><?= h($error) ?></p>
      </section>
<?php ELSE: ?>
      <section>
        <h2>登録中のキーワード</h2>
<?php IF($keywords): ?>
        <p>クロールされる順番で表示しています。</p>
        <table>
          <tr>
            <th>キーワード</th>
            <th class="numeric">重要度</th>
          </tr>
<?php FOREACH($keywords as $keyword_record): ?>
          <tr>
            <td><?= h($keyword_record["keyword"]) ?></td>
            <td><?= h($keyword_record["importance"])?></td>
          </tr>
<?php ENDFOREACH; ?>
        </table>
<?php ELSE: ?>
        <p>キーワードが登録されていません。</p>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
