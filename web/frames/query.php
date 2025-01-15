<?php
require_once "./modules/functions.php";

function banned($script) {
  return preg_match("/<\/script(\/| |>)/i", $script) ? true : false;
}

$queries = json_decode(queries(), true);
?>
<script>
const queries = {};
<?php FOREACH($queries as $name => $query): ?>
<?php IF(!banned($query) && !banned(json_encode($name))): ?>
queries[<?= json_encode($name) ?>] = (<?= $query ?>);
<?php ENDIF; ?>
<?php ENDFOREACH; ?>
</script>
<script defer src="./assets/query.js"></script>
