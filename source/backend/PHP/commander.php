<?php

function getPrognostication($latitude, $longitude, $date) {
    $python_path = "../Python/xg_dewst/xg_dewst.py";

    $escaped_latitude = escapeshellarg($latitude);
    $escaped_longitude = escapeshellarg($longitude);
    $date = escapeshellarg($date);

    $command = "python3 $python_path $escaped_latitude $escaped_longitude $date";

    $output = shell_exec($command);

    if (empty($output)) {
        return null;
    }

    return $output;
}

?>