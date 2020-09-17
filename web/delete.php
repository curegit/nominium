<?php
require_once "./modules/auth.php";
require_once "./modules/functions.php";

try {
  $pdo = open_db();
  $deletes = array_filter(isset($_POST["deletes"]) ? (array)$_POST["deletes"] : [], "is_numeric");
  if (!empty($deletes)) {
    $holders = implode(", ", array_fill(0, count($deletes), "?"));
    $stmt = $pdo->prepare("SELECT * FROM keyword WHERE id IN ($holders)");
    $stmt->execute($deletes);
    $deleted = $stmt->fetchAll();
    $stmt = $pdo->prepare("DELETE * FROM keyword WHERE id IN ($holders)");
    $stmt->execute($deletes);
  }
  $stmt = $pdo->query("SELECT * FROM keyword");
  $keywords = $stmt->fetchAll();
  $error = false;
} catch (PDOException $e) {
  $error = $e->getMessage();
}

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
