<?php
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "test_automation";  

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT test_name, url, status, error_message, execution_time, timestamp FROM test_results";
$result = $conn->query($sql);

$test_results = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $test_results[] = $row;
    }
} else {
    echo "No results found";
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 8px 12px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background-color: #f4f4f4;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .status-passed {
            color: green;
        }

        .status-failed {
            color: red;
        }

        .error-message {
            max-width: 300px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
</head>
<body>
    <h1>Test Results</h1>
    <table>
        <thead>
            <tr>
                <th>Test Name</th>
                <th>URL</th>
                <th>Status</th>
                <th>Error Message</th>
                <th>Execution Time (s)</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($test_results as $row): ?>
                <tr>
                    <td><?php echo $row['test_name']; ?></td>
                    <td><?php echo $row['url']; ?></td>
                    <td class="<?php echo $row['status'] == 'Passed' ? 'status-passed' : 'status-failed'; ?>">
                        <?php echo $row['status']; ?>
                    </td>
                    <td class="error-message"><?php echo $row['error_message'] ?: 'N/A'; ?></td>
                    <td><?php echo number_format($row['execution_time'], 2); ?></td>
                    <td><?php echo date("Y-m-d H:i:s", strtotime($row['timestamp'])); ?></td> 
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</body>
</html>
