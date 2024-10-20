
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prognostication Page</title>

    <link rel="stylesheet" href="./components/general.css">
    <link rel="stylesheet" href="./components/prog.css">

</head>
<body style="background:darkred;">

    <div class="menu-bar">
        <div class="button-container">
            <button class="home-button" onclick="location.href='../index.php'">Home</button>
            <button class="countries-button" onclick="location.href='./countries.php'">Countries</button>
            <button class="rankings-button" onclick="location.href='./rankings.html'">Rankings</button>
            <button class="prognostication-button" onclick="location.href='./prognostication.php'">Prognostication</button>
            <button class="newsletter-button" onclick="location.href='./newsletter.html'">Newsletter</button>
        </div>
    </div> 

    <div class="form-container">
    <form action="" method="get" id="form-id">
        <div class="input-box">
            <label for="lat">Latitude:</label><br>
            <input type="number" id="lat" name="lat" required step="any"><br>
        </div>
        <div class="input-box">
            <label for="long">Longitude:</label><br>
            <input type="number" id="long" name="long" required step="any"><br>
        </div>
        <div class="calendar" style="position:absolute; left: 38%;">
            <label for="date"></label>
            <input type="date" id="date" name="date" required><br>
        </div>
        <br>
        <br>
        <input type="submit" value="Submit">
    </form> 
    </div>
    
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

if (isset($result) && isset($result['data']) && is_array($result['data'])) {
    $location = $result['data'][0];
    $historical_data = $result['data'][1];
    $prediction_data = $result['data'][2];
?>

<h2 style="position: absolute; right: 25%; top: 70vh; font-size: 40px; color: white; 
    font-family: Roobert, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 
    'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; text-align: center;">
    Weather and Vapor-pressure Deficit Data for<br><?php echo htmlspecialchars($location); ?>
</h2>
<table border="1">
    <thead>
        <tr>
            <th style="font-weight: bold;">Stats</th>
            <?php
            foreach (array_keys($historical_data) as $date) {
                echo '<th>' . htmlspecialchars($date) . '</th>';
            }
            foreach (array_keys($prediction_data) as $date) {
                echo '<th>Prediction ' . htmlspecialchars($date) . '</th>';
            }
            ?>
        </tr>
    </thead>
    <tbody>
        <?php 
        $metrics = [
            'Longitude',
            'Latitude',
            'tempmin' => 'Min Temperature',
            'tempmax' => 'Max Temperature',
            'tempmean' => 'Mean Temperature',
            'tdmean' => 'Mean TD',
            'vpdmin' => 'Min VPD',
            'vpdmax' => 'Max VPD'
        ];

        foreach ($metrics as $key => $label) {
            if (is_numeric($key)) {
                $key = $label;
                $label = ucfirst($label);
            }

            echo '<tr>';
            echo '<td>' . htmlspecialchars($label) . '</td>';
            
            // Historical data
            foreach ($historical_data as $dayData) {
                if (isset($dayData[$key])) {
                    echo '<td>' . htmlspecialchars($dayData[$key]) . '</td>';
                } else {
                    echo '<td></td>';
                }
            }
            
            // Prediction data
            foreach ($prediction_data as $dayData) {
                if (isset($dayData[$key])) {
                    echo '<td>' . htmlspecialchars($dayData[$key]) . '</td>';
                } else {
                    echo '<td></td>';
                }
            }
            
            echo '</tr>';
        }
        ?>
    </tbody>
</table>

<?php
} else {
    echo '<p color: white;>No data available.</p>';
}
?>

</body>
</html>
