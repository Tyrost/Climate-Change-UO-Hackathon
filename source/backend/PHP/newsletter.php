<?php
// Database connection details
$servername = "localhost";  // Replace with your MySQL server (usually 'localhost')
$username = "root";         // Your MySQL username
$password = "";             // Your MySQL password (leave empty if no password is set)
$dbname = "SubscribersDB";  // The name of the database you created

// Create a connection to the MySQL database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check if the connection was successful
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if form data was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Collect and sanitize input
    $name = htmlspecialchars(strip_tags($_POST['name']));
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);

    // Prepare and bind the SQL statement to prevent SQL injection
    $stmt = $conn->prepare("INSERT INTO subscribers (name, email) VALUES (?, ?)");
    $stmt->bind_param("ss", $name, $email); // 'ss' means both variables are strings

    // Execute the statement and check if successful
    if ($stmt->execute()) {
        echo "<h2>Thank you, $name! You've been subscribed with $email.</h2>";
    } else {
        echo "Error: " . $stmt->error;
    }

    // Close the statement and connection
    $stmt->close();
}

$conn->close();
?>