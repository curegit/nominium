<?php
// HTMLエスケープ
function h($html) {
  return htmlspecialchars($html, ENT_QUOTES, "UTF-8");
}
