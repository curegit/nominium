<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $keyword = (string)filter_var($_POST["keyword"] ?? "");
  $importance = (float)filter_var($_POST["importance"] ?? 0, FILTER_VALIDATE_FLOAT);
  if ($keyword !== "" && $importance > 0 && $importance <= 1) {
    $stmt = $pdo->prepare("INSERT INTO keyword(keyword, importance) VALUES(?, ?)");
    $stmt->bindValue(1, $keyword);
    $stmt->bindValue(2, $importance);
    $stmt->execute();
  }
  $stmt = $pdo->query("SELECT * FROM keyword");
  $keywords = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  $error = $e->getMessage();
}

define("PAGE_TITLE", "キーワード登録");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($error): ?>
      <section>
        <h2>エラー</h2>
        <p><?= h($error) ?></p>
      </section>
<?php ELSE: ?>
<?php IF($keyword): ?>
      <section>
        <h2>操作の結果</h2>
        <p>登録されました：<?= h($keyword) ?></p>
      </section>
<?php ENDIF; ?>
      <section>
        <h2>キーワード登録</h2>
        <p>Register a new keyword</p>
        <form method="post">
          <label>Keyword: <input type="text" name="keyword"></label>
          <label>Importance: <input type="number" name="importance" min=0.01 max=1.0 step=0.01 value=0.8></label>
          <input type="submit" value="Register">
        </form>
      </section>
      <section>
        <h2>登録済みキーワード</h2>
        <ul>
<?php FOREACH($keywords as $keyword_record): ?>
         <li><?= h($keyword_record["keyword"]) ?> [<?= h($keyword_record["importance"]) ?>]</li>
<?php ENDFOREACH; ?>
        </ul>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
