<?php
$config = require __DIR__ . '/../../config/db.php'; 

try {
    // Create a new mysqli connection using the credentials
    $conn = new mysqli(
        $config['servername'], 
        $config['username'], 
        $config['password'], 
        $config['dbname']
    );

    // Check the connection
    if ($conn->connect_error) {
        throw new Exception("Connection failed: " . $conn->connect_error);
    }

    // Check for incoming request to delete results
    $data = json_decode(file_get_contents('php://input'), true);

    if (isset($data['delete_all']) && $data['delete_all'] === true) {
        // SQL query to delete all test results
        $sql = "DELETE FROM test_results";
        if ($conn->query($sql) === TRUE) {
            echo json_encode(['message' => 'All test results have been deleted.']);
        } else {
            echo json_encode(['message' => 'Error deleting results: ' . $conn->error]);
        }
    } elseif (isset($data['url'])) {
        // SQL query to delete test results for a specific URL
        $url = $conn->real_escape_string($data['url']);
        $sql = "DELETE FROM test_results WHERE url = '$url'";
        if ($conn->query($sql) === TRUE) {
            echo json_encode(['message' => "Test results for $url have been deleted."]);
        } else {
            echo json_encode(['message' => 'Error deleting results for this page: ' . $conn->error]);
        }
    } else {
        echo json_encode(['message' => 'Invalid request data.']);
    }

    // Close the database connection
    $conn->close();

} catch (Exception $e) {
    echo json_encode(['message' => 'Error: ' . $e->getMessage()]);
}
?>
