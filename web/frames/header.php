<?php
require_once __DIR__."/../modules/functions.php";
?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title><?= h(PAGE_TITLE) ?> | Nominium</title>
    <link href="./assets/style.css" rel="stylesheet">
    <link href="./assets/ziraffe.png" rel="icon">
    <link href="./assets/ziraffe.png" rel="apple-touch-icon">
  </head>
  <body>
    <header>
      <img src="./assets/ziraffe.png" alt="Ziraffe Symbol" width="120" height="120" style="float: left;">
      <h1>Nominium</h1>
      <p>Big Ziraffe is watching.</p>
    </header>
    <hr style="clear: both;">
    <nav>
      <p><a href="./">Home</a> | <a href="./register.php">Register</a> | <a href="./delete.php">Delete</a> | <a href="./logout.php">Logout</a>
    </nav>
    <hr>
