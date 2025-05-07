<?php
set_time_limit(300);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $pageUrl = $_POST['page_url'] ?? '';

    if ($pageUrl) {

        $parsedUrl = parse_url($pageUrl);
        $host = $parsedUrl['host'] ?? '';

        if (!$host) {
            echo json_encode([
                'status' => 'error',
                'message' => 'Invalid URL format.'
            ]);
            exit;
        }

        $fileBase = str_replace('.', '_', $host); 
        $scriptName = strtolower($fileBase) . '.py';

        $testPath = __DIR__ . "/../tests/$scriptName";
        $pythonPath = 'python'; 

        if (!file_exists($testPath)) {
            echo json_encode([
                'status' => 'error',
                'message' => "Test file not found: $scriptName"
            ]);
            exit;
        }

     
        $command = escapeshellcmd("$pythonPath $testPath");

  
        $output = shell_exec($command);

        echo json_encode([
            'status' => 'success',
            'output' => $output
        ]);
    } else {
        echo json_encode([
            'status' => 'error',
            'message' => 'No URL provided'
        ]);
    }
}
?>
