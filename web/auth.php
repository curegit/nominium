<?php
require_once "./settings/password.php";
switch (true) {
	case !isset($_SERVER["PHP_AUTH_USER"], $_SERVER["PHP_AUTH_PW"]):
	case $_SERVER["PHP_AUTH_USER"] !== username:
	case $_SERVER["PHP_AUTH_PW"] !== password:
		header("WWW-Authenticate: Basic realm=\"Enter username and password.\"");
		header("Content-Type: text/plain; charset=utf-8");
		die("You have to login to enter Ziraffem web.");
}
