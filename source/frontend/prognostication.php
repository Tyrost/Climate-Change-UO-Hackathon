
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prognostication Page</title>
</head>
<body>

    <form action="" method="get" id="form-id">
        <label for="lat">Latitude:</label><br>
        <input type="number" id="lat" name="lat" required step="any"><br>
        
        <label for="long">Longitude:</label><br>
        <input type="number" id="long" name="long" required step="any"><br>

        <label for="date">Date:</label><br>
        <input type="date" id="date" name="date" required><br>

        <input type="submit" value="Submit">
    </form>
    
<?php

function getPrognostication($latitude, $longitude, $date) {
    $python_path = "../backend/Python/xg_dewst/xg_dewst.py";

    if (!is_numeric($latitude) || !is_numeric($longitude) || !preg_match("/^\d{4}-\d{2}-\d{2}$/", $date)) {
        throw new InvalidArgumentException("Invalid input parameters");
    }

    $escaped_latitude = escapeshellarg($latitude);
    $escaped_longitude = escapeshellarg($longitude);
    $escaped_date = escapeshellarg($date);

    $command = "python3 $python_path $escaped_latitude $escaped_longitude $escaped_date";

    $output = shell_exec($command);

    if ($output === null) {
        throw new RuntimeException("Failed to execute Python script");
    }

    $data = json_decode($output, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new RuntimeException("Failed to parse JSON output: " . json_last_error_msg());
    }

    return $data;
}

$result = [];

try {
    $latitude = $_GET["lat"] ?? null;
    $longitude = $_GET["long"] ?? null;
    $date = $_GET["date"] ?? null;

    if (!isset($latitude) || !isset($longitude) || !isset($date)) {
        throw new InvalidArgumentException("Missing required parameters");
    }

    $prognostication_data = getPrognostication($latitude, $longitude, $date);

    $result = [
        'status' => 'success',
        'data' => $prognostication_data
    ];

} catch (InvalidArgumentException $e) {
    $result = [
        'status' => 'error',
        'message' => $e->getMessage()
    ];
} catch (RuntimeException $e) {
    $result = [
        'status' => 'error',
        'message' => $e->getMessage()
    ];
} catch (Exception $e) {
    $result = [
        'status' => 'error',
        'message' => 'An unexpected error occurred'
    ];
}

// print_r($result);
?>

<!-- ---------------------------------------------------------------- -->

<table id="dataTable">

<div class="table-container">
    <table id = "stats" style="float: left" border="1">
    <thead>
        <tr>
        <th>Stats</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">Â°F</td>
        </tr>
        <tr>
            <td>Temp (min)</td>
        </tr>
        <tr>
            <td>Temp (max)</td>
        </tr>
        <tr>
            <td>Temp (mean)</td>
        </tr>
        <tr>
            <td>VPD (min)</td>
        </tr>
        <tr>
            <td>VPD (max)</td>
        </tr>
    </tbody>
    <!-- TABLE OF ALREADY EXISTENT DATES -->
    <table id = "input" style="float: left" border="1">
    <thead>
        <tr> 
            <th>Day 1</th>
            <th>Day 2</th>
            <th>Day 3</th>
            <th>Day 4</th>
            <th>Day 5</th>
        </tr>
    </thead>
    <tbody>

    <!-- Takes JS file and inputs data here -->

    </tbody>
    </table>

    <!-- TABLE OF PROGNOSTICATED DATES -->

    <table id="prog" style="float: left;" border="1">
    <thead>
    <tr>
        <th>Day 1</th>
        <th>Day 2</th>
        <th>Day 3</th>
        <th>Day 4</th>
        <th>Day 5</th>
    </tr>
    </thead>
    <tbody>
    
    <!-- Takes JS file and inputs data here -->

    </tbody>
    </table>
</div>


<script src="../backend/JS/moment.min.js"></script> 
<script src="../backend/JS/progtable.js"></script>

</body>
</html>
