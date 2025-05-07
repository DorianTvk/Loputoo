<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Automation Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class'
        };
    </script>
    <style>
        .logo {
            max-width: 200px;
        }
    </style>
</head>

<body class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen flex items-center justify-center transition duration-300">

    <div class="absolute top-5 right-5">
        <button id="themeToggle" class="absolute top-4 right-4 p-2 bg-gray-300 dark:bg-gray-700 rounded">
            🌙
        </button>
    </div>

    <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-10 flex flex-col items-center gap-6 text-center max-w-md w-full">
        <img src="img/vdisain-logo-white.png" alt="Light Logo" class="logo block dark:hidden">
        <img src="img/vdisain-logo-dark.png" alt="Dark Logo" class="logo hidden dark:block">

        <form id="searchForm" class="w-full flex flex-col items-center gap-4">
            <input
                type="text"
                id="pageUrl"
                placeholder="Enter Page URL to Test"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                required>
            <div class="flex gap-4">
                <button
                    type="submit"
                    id = "runButton"
                    class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded transition ">
                    Run Test
                </button>
                <button
                    type="button"
                    id="stopButton"
                    class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition ">
                    Stop Test
                </button>
            </div>
        </form>

        <div id="loadingSpinner" class="hidden flex justify-center items-center mt-4">
            <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-green-600"></div>
        </div>

        <div class="flex gap-4">
            <a href="results.php" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition">
                View Test Results
            </a>
            <a href="visual_results.php" class="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition">
                View Visual Results
            </a>
        </div>
    </div>

    <script>
        const toggleBtn = document.getElementById('themeToggle');
        toggleBtn.addEventListener('click', () => {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });

        const form = document.getElementById('searchForm');
        const loadingSpinner = document.getElementById('loadingSpinner');
        const runButton = document.getElementById('runButton');
        const stopButton = document.getElementById('stopButton');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const pageUrl = document.getElementById('pageUrl').value.trim();

            if (!pageUrl) {
                alert('Please enter a URL.');
                return;
            }

            loadingSpinner.classList.remove('hidden');
            runButton.disabled = true;
            stopButton.disabled = false;

            controller = new AbortController();
            const {
                signal
            } = controller;

            try {
                const response = await fetch('run_test.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        page_url: pageUrl
                    }),
                    signal
                });

                const result = await response.json();

                if (result.status === 'success') {
                    alert('✅ Test run successfully!\n\nOutput:\n' + result.output);
                } else {
                    alert('❌ Error: ' + result.message);
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    alert('🛑 Test manually stopped.');
                } else {
                    console.error('Error:', error);
                    alert('An unexpected error occurred.');
                }
            } finally {
                loadingSpinner.classList.add('hidden');
                runButton.disabled = false;
                stopButton.disabled = true;
            }
        });

        stopButton.addEventListener('click', () => {
            if (controller) {
                controller.abort();
            }
        });

        stopButton.disabled = true;
    </script>

</body>

</html>