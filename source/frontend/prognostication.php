
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
    
</body>
</html>
