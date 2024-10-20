<?php

// Input Newsletter User data onto SQL LocalHost DB

$name = $_POST["name"];
$email = $_POST["email"];

$host = '127.0.0.1';
$port = '3306';
$db = 'uohackathon2024';
$dns = "mysql:host=$host;port=$port;dbname=$db";

$username = 'root';
$password = 'M12n2B3v4!';

$conn = new PDO($dns, $username, $password);

$query="INSERT INTO newsletter(name, email) VALUES (:name, :email);";

$statement = $conn->prepare($query);

$statement->bindValue(":name", $name);
$statement->bindValue(":email", $email);

$statement->execute();

// $users = $statement->fetchAll(PDO::FETCH_ASSOC);
?>