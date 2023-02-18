<?php
require_once "./modules/auth.php";
require_once "./modules/csrf.php";

$logout = $_SERVER["REQUEST_METHOD"] === "POST";
?>
<?php IF($logout): ?>
<?php http_response_code(401); ?>
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>ログアウト</title>
  </head>
  <body>
    <p>ログアウトを要求しました。</p>
  </body>
</html>
<?php ELSE: ?>
<?php define("PAGE_TITLE", "ログアウト"); ?>
<?php include "./frames/header.php"; ?>
    <main>
      <section>
        <h2>ログアウト操作</h2>
        <p>ログアウト要求を発行できます。</p>
        <form method="post">
          <input type="submit" value="ログアウトする">
        </form>
      </section>
    </main>
<?php include "./frames/footer.php"; ?>
<?php ENDIF; ?>
