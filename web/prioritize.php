<?php
require_once "./modules/auth.php";
require_once "./modules/csrf.php";
require_once "./modules/functions.php";

try {
  $updated = false;
  $pdo = open_db();
  $keywords = array_filter(isset($_POST["keywords"]) ? (array)$_POST["keywords"] : [], "is_numeric");
  $importances = array_filter(isset($_POST["importances"]) ? (array)$_POST["importances"] : [], "is_numeric");
  $sends = array_filter(isset($_POST["send"]) ? (array)$_POST["send"] : [], "is_numeric");
  $hooks = array_filter(isset($_POST["hook"]) ? (array)$_POST["hook"] : [], "is_numeric");
  for ($i = 0; $i < count($keywords) && $i < count($importances); $i++) {
    $send = in_array($keywords[$i], $sends);
    $hook = in_array($keywords[$i], $hooks);
    $stmt = $pdo->prepare("UPDATE keyword SET importance = ?, send = ?, hook = ? WHERE id = ?");
    $stmt->bindValue(1, $importances[$i]);
    $stmt->bindValue(2, $send ? 1 : 0);
    $stmt->bindValue(3, $hook ? 1 : 0);
    $stmt->bindValue(4, $keywords[$i]);
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

define("PAGE_TITLE", "割り付け変更");
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
        <h2>重要度と通知動作の変更</h2>
<?php IF($keywords): ?>
        <p>表中に変更後の値を入力してください。</p>
        <form method="post">
          <table>
            <thead>
              <tr>
                <th>キーワード</th>
                <th class="numeric">現在重要度</th>
                <th class="numeric">変更後重要度</th>
                <th class="symbolic">メール</th>
                <th class="symbolic">フック</th>
              </tr>
            </thead>
            <tbody>
<?php FOREACH($keywords as $keyword_record): ?>
              <tr>
                <td><?= h($keyword_record["keyword"]) ?></td>
                <td><?= h($keyword_record["importance"]) ?></td>
                <td>
                  <input type="hidden" name="keywords[]" value="<?= h($keyword_record["id"]) ?>">
                  <input type="number" name="importances[]" size=12 min=0.01 max=1.0 step=0.01 value="<?= h($keyword_record["importance"]) ?>">
                </td>
                <td class="symbolic">
                  <input type="checkbox" name="send[]" value="<?= h($keyword_record["id"]) ?>" <?= $keyword_record["send"] ? "checked" : "" ?>>
                </td>
                <td class="symbolic">
                  <input type="checkbox" name="hook[]" value="<?= h($keyword_record["id"]) ?>" <?= $keyword_record["hook"] ? "checked" : "" ?>>
                </td>
              </tr>
<?php ENDFOREACH; ?>
            </tbody>
          </table>
          <input type="submit" value="変更する">
        </form>
<?php ELSE: ?>
        <p>キーワードが登録されていません。</p>
<?php ENDIF; ?>
      </section>
<?php ENDIF; ?>
    </main>
<?php include "./frames/footer.php"; ?>
