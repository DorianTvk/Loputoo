<?php
$config = require __DIR__ . '/../../config/db.php';

$conn = new mysqli(
    $config['servername'],
    $config['username'],
    $config['password'],
    $config['dbname']
);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT test_name, url, status, error_message, execution_time, timestamp, screenshot_path, test_type FROM test_results";
$result = $conn->query($sql);

$regular_results = [];
$visual_results = [];

if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        // Separate regular tests and visual tests based on the test_type field
        if ($row['test_type'] == 'regular') {
            $regular_results[] = $row;
        } elseif ($row['test_type'] == 'visual') {
            $visual_results[] = $row;
        }
    }
}

$conn->close();
?>