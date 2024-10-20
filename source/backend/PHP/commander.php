<?php

function getPrognostication($latitude, $longitude, $date) {
    $python_path = "../Python/xg_dewsf/xg_dewsf.py";

    $escaped_latitude = escapeshellarg($latitude);
    $escaped_longitude = escapeshellarg($longitude);
    $escaped_start_date = escapeshellarg($date);


    $command = "python3 $python_path $escaped_latitude $escaped_longitude $date";

    $output = shell_exec($command);

    if (empty($output)) {
        return null;
    }

    return $output;
}

?>