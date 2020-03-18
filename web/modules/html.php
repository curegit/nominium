<?php
// HTML メタ文字のエスケープ
function h($html)
{
  return htmlspecialchars($html, ENT_QUOTES, "UTF-8");
}
