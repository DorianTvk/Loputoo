<?php
require __DIR__ . '/includes/get_test_results.php';
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results</title>

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
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen p-4">

    <button onclick="window.history.back()" class="absolute top-4 left-4 p-2 bg-gray-300 dark:bg-gray-700 rounded text-white">
        ← Back
    </button>

    <button id="darkToggle" class="absolute top-4 right-4 p-2 bg-gray-300 dark:bg-gray-700 rounded">🌙</button>

    <div class="max-w-7xl mx-auto">
        <h1 class="text-3xl font-bold mb-6 text-center">Test Results</h1>

        <div class="flex justify-end space-x-2 mb-4">
            <button onclick="deleteAllResults()" class="bg-red-500 text-white px-4 py-2 rounded">Delete All</button>
        </div>

        <?php
        $grouped = [];
        foreach ($regular_results as $result) {
            $grouped[$result['url']][] = $result;
        }
        ?>

        <?php foreach ($grouped as $url => $results): ?>
            <div class="mb-6 border rounded-lg shadow-md overflow-hidden">
                <div class="bg-gray-300 dark:bg-gray-700 px-4 py-2 flex justify-between items-center cursor-pointer" onclick="toggleGroup(this)">
                    <h2 class="font-semibold text-lg">🔗 <?php echo $url; ?></h2>
                    <button onclick="deletePageResults('<?php echo $url; ?>'); event.stopPropagation();" class="bg-red-400 hover:bg-red-600 text-white px-2 py-1 rounded text-sm">Delete Page Results</button>
                </div>
                <div class="hidden group-content">
                    <table class="min-w-full table-auto border border-gray-200 dark:border-gray-700">
                        <thead>
                            <tr class="bg-gray-200 dark:bg-gray-800">
                                <th class="px-4 py-2 border">Test Name</th>
                                <th class="px-4 py-2 border">Status</th>
                                <th class="px-4 py-2 border">Error Message</th>
                                <th class="px-4 py-2 border">Execution Time</th>
                                <th class="px-4 py-2 border">Date</th>
                                <th class="px-4 py-2 border">Screenshot</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($results as $row): ?>
                                <tr class="border-t border-gray-200 dark:border-gray-700">
                                    <td class="px-4 py-2 border dark:border-gray-700"><?php echo $row['test_name']; ?></td>
                                    <td class="px-4 py-2 border dark:border-gray-700 <?php echo $row['status'] === 'Passed' ? 'text-green-600' : 'text-red-600'; ?>"><?php echo $row['status']; ?></td>
                                    <td class="px-4 py-2 border dark:border-gray-700 max-w-xs truncate" title="<?php echo $row['error_message']; ?>">
                                        <?php echo $row['error_message'] ?: 'N/A'; ?>
                                    </td>
                                    <td class="px-4 py-2 border dark:border-gray-700"><?php echo number_format($row['execution_time'], 2); ?></td>
                                    <td class="px-4 py-2 border dark:border-gray-700"><?php echo date("Y-m-d H:i:s", strtotime($row['timestamp'])); ?></td>
                                    <td class="px-4 py-2 border dark:border-gray-700">
                                        <?php if (!empty($row['screenshot_path'])): ?>
                                            <a href="/<?php echo $row['screenshot_path']; ?>" class="text-blue-500 underline" target="_blank">View</a>
                                        <?php else: ?>
                                            N/A
                                        <?php endif; ?>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        <?php endforeach; ?>

        <div class="mt-10">
            <h2 class="text-2xl font-semibold text-center mb-4">Test Summary</h2>
            <canvas id="testChart" class="max-w-md mx-auto"></canvas>
        </div>
    </div>

    <script>

        const toggle = document.getElementById('darkToggle');
        toggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
        });

        function toggleGroup(header) {
            const content = header.nextElementSibling;
            content.classList.toggle('hidden');
        }


        function deleteResults(data) {
            if (confirm(data.message)) {
                fetch('includes/delete_results.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }).then(() => location.reload());
            }
        }


        function deleteAllResults() {
            deleteResults({
                delete_all: true,
                message: 'Are you sure you want to delete all test results?'
            });
        }

        function deletePageResults(url) {
            deleteResults({
                url,
                message: `Delete all test results for ${url}?`
            });
        }


        const ctx = document.getElementById('testChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Passed', 'Failed'],
                datasets: [{
                    data: [
                        <?php echo count(array_filter($regular_results, fn($r) => $r['status'] === 'Passed')); ?>,
                        <?php echo count(array_filter($regular_results, fn($r) => $r['status'] !== 'Passed')); ?>
                    ],
                    backgroundColor: ['#10B981', '#EF4444']
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    </script>
</body>

</html>