<?php

require_once '../backend/PHP/commander.php';
$data = [];
$latitude = isset($_GET["lat"]) ? $_GET["lat"]:null;
$longitude = isset($_GET["long"]) ? $_GET["long"]:null;
$date = isset($_GET["date"]) ? $_GET["date"]:null;

if ($latitude && $longitude && $date) {

    $data = getPrognostication($latitude, $longitude, $date);

    $data = $data ? json_decode($data, true) : [];
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action= "" method="get" id="form-id">
        <label for="lat">Latitude:</label><br>
        <input type="number" id="lat" name="lat"><br>
        <label for="long">Longitude:</label><br>
        <input type="number" id="long" name="long">

        <label for="start">Date</label><br>
        <input type="date" name="date"><br>

        <input type="submit" value="Submit">
      </form>
</body>
</html>