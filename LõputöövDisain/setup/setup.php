<?php
$servername = "localhost";  
$port = 3306; 
$username = "root";  
$password = "1234";  
$dbname = "test_automation";
$maxRetries = 10; 
$retryDelay = 5;   

for ($i = 0; $i < $maxRetries; $i++) {
    echo "Attempt " . ($i + 1) . ": Trying to connect to MySQL...\n";
    $conn = @new mysqli($servername, $username, $password, "", $port);
    if ($conn->connect_error) {
        echo "Attempt " . ($i + 1) . ": Failed to connect to MySQL. Error: " . $conn->connect_error . "\n";
        sleep($retryDelay);
    } else {
        echo "Connected successfully to MySQL!\n";
        break;
    }
}

if ($conn->connect_error) {
    die("Connection failed after $maxRetries attempts: " . $conn->connect_error);
}

$sql = "CREATE DATABASE IF NOT EXISTS $dbname";
if ($conn->query($sql) === TRUE) {
    echo "Database created successfully or already exists.\n";
} else {
    echo "Error creating database: " . $conn->error . "\n";
}

$conn->select_db($dbname);

$table_sql = "CREATE TABLE IF NOT EXISTS test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(255) NOT NULL,
    url VARCHAR(500) NOT NULL,
    status ENUM('Passed', 'Failed', 'Skipped') NOT NULL,
    error_message TEXT,
    execution_time FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)";

if ($conn->query($table_sql) === TRUE) {
    echo "Table test_results created successfully or already exists.\n";
} else {
    echo "Error creating table: " . $conn->error . "\n";
}

$conn->close();
?>
