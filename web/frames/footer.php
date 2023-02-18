<?php
require_once "./modules/functions.php";

$version = rtrim(file_get_contents(__DIR__."/../../VERSION"));
?>
    <footer>
      <span>Nominium <?= h($version) ?> Web Interface on PHP <?= h(phpversion()) ?></span>
    </footer>
  </body>
</html>
