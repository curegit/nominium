<?php
require_once "./modules/auth.php";
require_once "./modules/csrf.php";
require_once "./modules/functions.php";

try {
  $updated = false;
  $pdo = open_db();
  $keywords = array_filter(isset($_POST["keywords"]) ? (array)$_POST["keywords"] : [], "is_numeric");
  for ($i = 0; $i < count($keywords); $i++) {
    $stmt = $pdo->prepare("UPDATE keyword SET priority = ? WHERE id = ?");
    $stmt->bindValue(1, count($keywords) - $i);
    $stmt->bindValue(2, $keywords[$i]);
    $stmt->execute();
    $updated = true;
  }
  $stmt = $pdo->query("SELECT * FROM keyword ORDER BY priority DESC");
  $keywords = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  http_response_code(500);
  $error = $e->getMessage();
}

define("PAGE_TITLE", "並べ替え");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($updated): ?>
      <section>
        <h2>操作の結果</h2>
        <p>更新されました。</p>
      </section>
<?php ENDIF; ?>
<?php IF($error): ?>
      <section>
        <h2>エラー</h2>
        <p><?= h($error) ?></p>
      </section>
<?php ELSE: ?>
      <section>
        <h2>キーワードの並べ替え</h2>
<?php IF($keywords): ?>
        <p>クロールしたい順番にキーワードを並べ替えできます。（要ドラッグ操作）</p>
        <script defer src="./assets/reorder.js"></script>
        <form method="post">
          <ol class="reorderable">
<?php FOREACH($keywords as $keyword_record): ?>
            <li draggable="true"><input type="hidden" name="keywords[]" value="<?= h($keyword_record["id"]) ?>"><?= h($keyword_record["keyword"]) ?></li>
<?php ENDFOREACH; ?>
          </ol>
          <input type="submit" value="確定する">
        </form>
<?php ELSE: ?>
        <p>キーワードが登録されていません。</p>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
