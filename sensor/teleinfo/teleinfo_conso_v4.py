#!/usr/bin/php5
<?php

header('Content-type: text/html; charset=utf-8');

require_once('teleinfo_func_v3.php');

computeLastDayConso();

?>

function computeLastDayConso()
{


$today = strtotime('today 00:00:00');
$yesterday = strtotime("-1 day 00:00:00");

$link = mysqli_connect('192.168.1.56', 'pi', '66446644', 'teleinfo_v2') \
        or die('Impossible de se connecter : '.mysqli_error());

// $query = "SELECT MAX(timestamp) AS timestamp, MAX(base) AS total_base, ((MAX(base) - MIN(base)) / 1000) AS daily_base FROM puissance
            // WHERE; timestamp >= $yesterday; AND; timestamp < $today; AND; base != ''; GROUP; BY; DATE_FORMAT(timestamp, '%d-%m-%Y');";
$query = "SELECT MAX(timestamp) AS timestamp, MAX(base) AS total_base, ((MAX(base) - MIN(base)) / 1000) AS daily_base FROM puissance WHERE timestamp >= $yesterday AND timestamp < $today AND base != '';";

$result = mysqli_query($link,$query) or die('Échec de la requête : '.mysqli_error($link));


$previousDay = mysqli_fetch_array($result, MYSQLI_ASSOC);

$query = 'CREATE TABLE IF NOT EXISTS conso (timestamp INTEGER, total_base INTEGER, daily_base REAL);'; // cree; la; table; conso; si; elle; n; 'existe pas
$result = mysqli_query($link,$query) or die('Échec de la requête : '.mysqli_error($link));


$query = "INSERT INTO conso (timestamp, total_base, daily_base) VALUES \
(".$previousDay['timestamp'].
", ".$previousDay['total_base'].
", ".$previousDay['daily_base'].
");";
$result = mysqli_query($link,$query) or die('Échec de la requête : '.mysqli_error($link));
mysqli_close($link);
}
