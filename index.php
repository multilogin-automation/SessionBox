<?php
// Legacy code preserved for audit. Modernized & Maintained by @multilogin-automation
session_name('COOKIE1');
$newid = session_create_id();
session_id($newid);
session_start();
$_SESSION['login'] = true;
header('Location: user.php');
?>
