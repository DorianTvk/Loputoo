<?php

$config = require __DIR__ . '/../config/db.php';
$conn = new mysqli($config['servername'], $config['username'], $config['password'], $config['dbname']);
$results = [];


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['delete_all'])) {
        $conn->query("DELETE FROM test_results WHERE diff_path IS NOT NULL AND test_type = 'visual'");

        $dirs = ['baseline', 'new', 'diff'];
        foreach ($dirs as $dir) {
            $path = __DIR__ . "/../screenshots/$dir";
            if (is_dir($path)) {
                $files = glob("$path/*.png");
                foreach ($files as $file) {
                    unlink($file);
                }
            }
        }
    }

    if (isset($_POST['delete_selected']) && isset($_POST['selected'])) {
        $ids = array_map('intval', $_POST['selected']);
        $idList = implode(',', $ids);
        $conn->query("DELETE FROM test_results WHERE id IN ($idList)");
    }

    header("Location: visual_results.php");
    exit;
}

if (!$conn->connect_error) {
    $sql = "SELECT id, test_name, timestamp, baseline_path, new_path, diff_path, error_message, status  
            FROM test_results 
            WHERE diff_path IS NOT NULL AND test_type = 'visual'
            ORDER BY timestamp DESC";
    $result = $conn->query($sql);

    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $results[] = $row;
        }
    }

    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Visual Regression Results</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class'
        };

        if (localStorage.getItem('theme') === 'dark' ||
            (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        }
    </script>
</head>

<body class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-10">

    <button onclick="window.history.back()" class="absolute top-4 left-4 p-2 bg-gray-300 dark:bg-gray-700 rounded text-white">
        ← Back
    </button>

    <div class="absolute top-5 right-5">
        <button id="darkToggle" class="p-2 bg-gray-300 dark:bg-gray-700 rounded">
            🌙
        </button>
    </div>

    <h1 class="text-3xl font-bold mb-6 mt-10">🖼️ Visual Regression Differences</h1>

    <?php if (empty($results)): ?>
        <p>No visual differences found.</p>
    <?php else: ?>
        <form method="POST" onsubmit="return confirm('Are you sure you want to delete?');">
            <div class="flex gap-4 mb-6">
                <button type="submit" name="delete_all" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">🗑️ Delete All</button>
                <button type="submit" name="delete_selected" class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600">❌ Delete Selected</button>
            </div>

            <?php foreach ($results as $row): ?>
                <div class="bg-white dark:bg-gray-800 p-6 mb-10 shadow-md rounded-lg relative">
                    <input type="checkbox" name="selected[]" value="<?= $row['id'] ?>" class="absolute top-4 left-4 w-5 h-5">
                    <h2 class="text-xl font-semibold ml-8"><?= htmlspecialchars($row['test_name']) ?></h2>
                    <p class="text-sm text-gray-600 ml-8"><?= $row['timestamp'] ?> — <?= htmlspecialchars($row['error_message'] ?? '') ?></p>
                    <div class="grid grid-cols-3 gap-4 mt-4">
                        <div>
                            <p class="font-medium mb-1">🧱 Baseline</p>
                            <img src="<?= ($row['baseline_path']) ?>" alt="Baseline Screenshot" class="w-full border">
                        </div>
                        <div>
                            <p class="font-medium mb-1">📸 New</p>
                            <img src="<?= ($row['new_path']) ?>" alt="New Screenshot" class="w-full border">
                        </div>
                        <div>
                            <p class="font-medium mb-1">⚠️ Diff</p>
                            <img src="<?= ($row['diff_path']) ?>" alt="Diff Screenshot" class="w-full border">
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </form>
    <?php endif; ?>

    <script>

        const toggle = document.getElementById('darkToggle');
        toggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
        });
    </script>
</body>

</html>