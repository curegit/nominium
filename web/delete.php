<?php
// 認証
require_once "./auth.php";
// インポート
require_once "./modules/html.php";
require_once "./modules/database.php";
// エラーメッセージなし
$error = "";
// エラー検証
try {
	// DB接続
	$pdo = open_db();
	// 削除IDが与えられていれば処理する
	$deletes = isset($_POST["deletes"]) ? (array)$_POST["deletes"] : [];
	$deletes = array_filter($deletes, "is_numeric");
	// 削除されるものを記録
	$deleted = [];
	foreach ($deletes as $del) {
		// 削除されるものを調べる
		$stmt = $pdo->prepare("SELECT * FROM keyword WHERE id = ?");
		$stmt->bindValue(1, $del);
		$stmt->execute();
		$deleted = array_merge($deleted, $stmt->fetchAll());
		// 削除する
		$stmt = $pdo->prepare("DELETE FROM keyword WHERE id = ?");
		$stmt->bindValue(1, $del);
		$stmt->execute();
	}
	// 一覧取得
	$stmt = $pdo->query("SELECT * FROM keyword");
	$keywords = $stmt->fetchAll();
// エラー時
} catch (PDOException $e) {
	$error = $e->getMessage();
}
// ページ変数
define("PAGE_TITLE", "Delete");
?>
<?php include "./frames/header.php"; ?>
<?php IF($error): ?>
    <section>
      <h2>Error</h2>
      <p><?= h($error) ?></p>
    </section>
<?php ELSE: ?>
<?php IF($deleted): ?>
    <section>
      <h2>Result</h2>
<?php FOREACH($deleted as $del): ?>
      <p>Deleted: <?= h($del["keyword"]) ?></p>
<?php ENDFOREACH; ?>
    </section>
<?php ENDIF; ?>
    <section>
      <h2>Delete</h2>
      <p>Delete keywords</p>
      <form method="post">
        <table>
          <tr>
            <th>Delete</th>
            <th>Keyword</th>
            <th>Importance</th>
          </tr>
<?php FOREACH($keywords as $keyword_record): ?>
          <tr>
            <td style="text-align: center"><input type="checkbox" name="deletes[]" value="<?= h($keyword_record["id"]) ?>"></td>
            <td><?= h($keyword_record["keyword"]) ?></td>
            <td style="text-align: right"><?= h($keyword_record["importance"])?></td>
          </tr>
<?php ENDFOREACH; ?>
        </table>
        <input type="submit" value="Delete">
      </form>
    </section>
<?php ENDIF; ?>
<?php include "./frames/footer.php"; ?>
