<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $deletes = array_filter(isset($_POST["deletes"]) ? (array)$_POST["deletes"] : [], "is_numeric");
  if ($deletes) {
    $holders = implode(", ", array_fill(0, count($deletes), "?"));
    $stmt = $pdo->prepare("SELECT * FROM filter WHERE id IN ($holders)");
    $stmt->execute($deletes);
    $deleted = $stmt->fetchAll();
    $stmt = $pdo->prepare("DELETE FROM filter WHERE id IN ($holders)");
    $stmt->execute($deletes);
  } else {
    $deleted = [];
  }
  $pattern = (string)filter_var($_POST["pattern"] ?? "");
  if ($pattern !== "") {
    $stmt = $pdo->prepare("INSERT INTO filter(pattern) VALUES(?)");
    $stmt->bindValue(1, $pattern);
    $stmt->execute();
  }
  $stmt = $pdo->query("SELECT * FROM filter");
  $filters = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  $error = $e->getMessage();
}

define("PAGE_TITLE", "フィルタ");
?>
<?php include "./frames/header.php"; ?>
    <main>
<?php IF($error): ?>
      <section>
        <h2>エラー</h2>
        <p><?= h($error) ?></p>
      </section>
<?php ELSE: ?>
<?php IF($pattern !== "" || $deleted): ?>
      <section>
        <h2>操作の結果</h2>
<?php FOREACH($deleted as $del): ?>
        <p>削除されました：<?= h($del["pattern"]) ?></p>
<?php ENDFOREACH; ?>
<?php IF($pattern !== ""): ?>
        <p>登録されました：<?= h($pattern) ?></p>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
      <section>
        <h2>新規フィルタ登録</h2>
        <p>合致を含んだ場合に通知をしないようにするタイトルの正規表現パターンを入力してください。</p>
        <form method="post">
          <label>パターン：<input type="text" name="pattern"></label>
          <input type="submit" value="登録する">
        </form>
      </section>
<?php IF($filters): ?>
      <section>
        <h2>登録済みフィルタの削除</h2>
        <p>削除するフィルタを選択してください。</p>
        <form method="post">
          <ul class="checklist">
<?php FOREACH($filters as $filter_record): ?>
            <li>
              <label><input type="checkbox" name="deletes[]" value="<?= h($filter_record["id"]) ?>"><?= h($filter_record["pattern"]) ?></label>
            </li>
<?php ENDFOREACH; ?>
          </ul>
          <input type="submit" value="削除する">
        </form>
      </section>
<?php ENDIF; ?>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
