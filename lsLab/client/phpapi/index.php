<?php
require('./index.html');
$jsonUrl = "./member.json";

if(file_exists($jsonUrl)){
	$json = file_get_contents($jsonUrl);
	$json = mb_convert_encoding($json, 'UTF8', 'ASCII,JIS,UTF8,EUC-JP,SJIS-WIN');
	$obj = json_decode($json, true);
	$obj = $obj;
}

header("Content-Type: application/json; charset=UTF-8");
header("X-Content-Type-Options: nosniff");

echo json_encode(
	$obj,
	JSON_HEX_TAG | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_HEX_AMP);



?>