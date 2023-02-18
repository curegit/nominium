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
        <h2>ログアウト要求</h2>
        <form method="post">
          <input type="submit" value="ログアウトする">
        </form>
      </section>
    </main>
<?php include "./frames/footer.php"; ?>
<?php ENDIF; ?>
