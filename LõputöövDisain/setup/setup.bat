@echo off
REM Setup Script for the Test Automation Project

REM Step 1: Check and Install PHP
php --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PHP is not installed. Installing PHP...
    REM Insert PHP installation steps here (e.g., download PHP installer and install)
    REM Example: wget https://windows.php.net/downloads/releases/php-8.2.13-nts-x64.zip -O php.zip
    REM Unzip and add PHP to PATH
    exit /b 1
) else (
    echo ✅ PHP is already installed.
)

REM Step 2: Check and Install Composer
composer --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Composer is not installed. Installing Composer...
    REM Download and install Composer
    REM Example: curl -sS https://getcomposer.org/installer | php
    REM Move Composer to a directory in PATH
    exit /b 1
) else (
    echo ✅ Composer is already installed.
)

REM Step 3: Check and Install Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed. Installing Node.js...
    REM Insert Node.js installation steps here (e.g., download Node.js installer and install)
    REM Example: wget https://nodejs.org/dist/v21.4.0/node-v21.4.0-x64.msi
    REM Execute Node.js installer
    exit /b 1
) else (
    echo ✅ Node.js is already installed.
)

REM Step 4: Check and Install MySQL
mysql --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ MySQL is not installed. Installing MySQL...
    REM Insert MySQL installation steps here (e.g., download MySQL installer and install)
    REM Example: wget https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-web-community-8.0.30.0.msi
    REM Execute MySQL installer
    exit /b 1
) else (
    echo ✅ MySQL is already installed.
)

REM Step 5: Start MySQL service (if not already running)
echo Starting MySQL service...
net start MySQL
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to start MySQL service! Exiting setup.
    exit /b 1
)
echo ✅ MySQL service started successfully.

REM Step 6: Check and Install Git
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git is not installed. Installing Git...
    REM Insert Git installation steps here (e.g., download Git installer and install)
    REM Example: wget https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/MinGit-2.42.0-64-bit.zip
    REM Unzip Git to a directory and add to PATH
    exit /b 1
) else (
    echo ✅ Git is already installed.
)

REM Step 7: Install PHP dependencies using Composer
echo Installing PHP dependencies...
composer install
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Composer installation failed! Exiting setup.
    exit /b 1
)

REM Step 8: Install vlucas/phpdotenv package (if not already installed)
echo Installing vlucas/phpdotenv package...
composer require vlucas/phpdotenv
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Installation of vlucas/phpdotenv failed! Exiting setup.
    exit /b 1
)

REM Step 9: Set up the environment by copying the .env.example to .env
echo Setting up environment variables...
if not exist ".env" (
    copy .env.example .env
    echo ✅ Environment variables setup completed.
) else (
    echo .env file already exists, skipping setup.
)

REM Step 10: Run the PHP database setup script
echo Running database setup...
php setup/db_setup.php
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Database setup failed! Exiting setup.
    exit /b 1
)

REM Step 11: Check if Python is installed, if not, install it
echo Checking Python installation...
python --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    REM You can add a download link for Python or handle this step manually
    REM For example:
    REM start https://www.python.org/downloads/
    exit /b 1
)
echo Python is installed.

REM Step 12: Check if pip is installed, if not, install it
echo Checking pip installation...
pip --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ pip installation failed! Exiting setup.
        exit /b 1
    )
    echo ✅ pip installed.
)

REM Step 13: Install Python dependencies from requirements.txt
echo Installing Python dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python dependencies installation failed! Exiting setup.
    exit /b 1
)
echo ✅ Python dependencies installed successfully.

REM Step 13: Install Sass globally using npm
echo Installing Sass...
npm install -g sass
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Sass installation failed! Exiting setup.
    exit /b 1
)
echo ✅ Sass installation completed.

REM Step 14: Display a success message
echo ✅ Setup completed successfully!
pause
