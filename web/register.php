<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $keyword = (string)filter_var($_POST["keyword"] ?? "");
  $importance = (float)filter_var($_POST["importance"] ?? 0, FILTER_VALIDATE_FLOAT);
  if ($keyword !== "") {
    $stmt = $pdo->prepare("INSERT INTO keyword(keyword, importance) VALUES(?, ?)");
    $stmt->bindValue(1, $keyword);
    $stmt->bindValue(2, $importance);
    $stmt->execute();
  }
  $stmt = $pdo->query("SELECT * FROM keyword ORDER BY priority DESC");
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
<?php IF($keyword !== ""): ?>
      <section>
        <h2>操作の結果</h2>
        <p>登録されました：<?= h($keyword) ?></p>
      </section>
<?php ENDIF; ?>
      <section>
        <h2>新規キーワード登録</h2>
        <p>検索キーワードと重要度を入力してください。</p>
        <form class="register" method="post">
          <label>キーワード：<input type="text" name="keyword"></label>
          <label>重要度：<input type="number" name="importance" min=0.01 max=1.0 step=0.01 value=0.8></label>
          <input type="submit" value="登録する">
        </form>
      </section>
<?php IF($keywords): ?>
      <section>
        <h2>登録済みキーワード</h2>
        <ul>
<?php FOREACH($keywords as $keyword_record): ?>
         <li><?= h($keyword_record["keyword"]) ?></li>
<?php ENDFOREACH; ?>
        </ul>
      </section>
<?php ENDIF; ?>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
