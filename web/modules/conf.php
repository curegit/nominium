<?php
// アプリケーション構成ファイルのパス
define("APP_INI", realpath(__DIR__."/../../conf/app.ini"));

// ユーザ設定ファイルのパス
define("SETTINGS_INI", realpath(__DIR__."/../../conf/settings.ini"));

// アプリケーション構成を返す
function get_app_conf()
{
  return parse_ini_file(APP_INI, true);
}

// ユーザ設定を返す
function get_settings()
{
  return parse_ini_file(SETTINGS_INI, true);
}
