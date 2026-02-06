<?php
header('Content-Type: application/json');

// ---- DB CONFIG ----
$host = "localhost";
$user = "YOUR_DB_USER";
$pass = "YOUR_DB_PASSWORD";
$dbname = "tih";

// ---- OPTIONAL API KEY ----
// If you want to protect this endpoint, set a key here and call:
// https://iitgtidf.com/xyz.php?key=YOUR_KEY
$required_key = "";
if ($required_key !== "") {
    $key = isset($_GET['key']) ? $_GET['key'] : "";
    if ($key !== $required_key) {
        echo json_encode(["error" => "Unauthorized"]);
        exit;
    }
}

// ---- CONNECT ----
$conn = new mysqli($host, $user, $pass, $dbname);
if ($conn->connect_error) {
    echo json_encode(["error" => "DB connection failed"]);
    exit;
}

// ---- QUERY ----
$sql = "SELECT * FROM doser ORDER BY id DESC";
$result = $conn->query($sql);

$data = [];
if ($result) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

echo json_encode([
    "status" => "success",
    "count" => count($data),
    "data" => $data
]);

$conn->close();