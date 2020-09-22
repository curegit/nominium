<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title><?= h(PAGE_TITLE) ?> | Nominium</title>
    <link href="./assets/style.css" rel="stylesheet">
    <link href="./assets/ziraffe.png" rel="icon">
  </head>
  <body>
    <header>
      <h1>Nominium – <?= h(PAGE_TITLE) ?></h1>
      <nav class="menu">
        <ul>
          <li><a href="./">ホーム</a></li>
          <li><a href="./register.php">登録</a></li>
          <li><a href="./delete.php">削除</a></li>
          <li><a href="./prioritize.php">重要度</a></li>
          <li><a href="./filter.php">フィルタ</a></li>
          <li><a href="./inspect.php">監査</a></li>
          <li><a href="./logout.php">ログアウト</a></li>
        </ul>
      </nav>
    </header>
