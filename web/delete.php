<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $deletes = array_filter(isset($_POST["deletes"]) ? (array)$_POST["deletes"] : [], "is_numeric");
  if ($deletes) {
    $holders = implode(", ", array_fill(0, count($deletes), "?"));
    $stmt = $pdo->prepare("SELECT * FROM keyword WHERE id IN ($holders)");
    $stmt->execute($deletes);
    $deleted = $stmt->fetchAll();
    $stmt = $pdo->prepare("DELETE FROM keyword WHERE id IN ($holders)");
    $stmt->execute($deletes);
  } else {
    $deleted = [];
  }
  $stmt = $pdo->query("SELECT * FROM keyword ORDER BY priority DESC");
  $keywords = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  $error = $e->getMessage();
}

define("PAGE_TITLE", "キーワード削除");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($error): ?>
      <section>
        <h2>エラー</h2>
        <p><?= h($error) ?></p>
      </section>
<?php ELSE: ?>
<?php IF($deleted): ?>
      <section>
        <h2>操作の結果</h2>
<?php FOREACH($deleted as $del): ?>
        <p>削除されました：<?= h($del["keyword"]) ?></p>
<?php ENDFOREACH; ?>
      </section>
<?php ENDIF; ?>
      <section>
        <h2>登録済みキーワードの削除</h2>
<?php IF($keywords): ?>
        <p>削除するキーワードを選択してください。</p>
        <form method="post">
          <ul class="checklist">
<?php FOREACH($keywords as $keyword_record): ?>
            <li>
              <label><input type="checkbox" name="deletes[]" value="<?= h($keyword_record["id"]) ?>"><?= h($keyword_record["keyword"]) ?></label>
            </li>
<?php ENDFOREACH; ?>
          </ul>
          <input type="submit" value="削除する">
        </form>
<?php ELSE: ?>
        <p>キーワードが登録されていません。</p>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
