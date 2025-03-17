# Ensure the script runs with administrator privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as Administrator!" -ForegroundColor Red
    exit 1
}

# Enable script execution policy
Set-ExecutionPolicy Bypass -Scope Process -Force

# Check if Chocolatey is installed, install if not
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
} else {
    Write-Host "Chocolatey is already installed."
}

# Install CMake using Chocolatey if not present
if (-not (Get-Command cmake -ErrorAction SilentlyContinue)) {
    Write-Host "Installing CMake..."
    choco install cmake -y
} else {
    Write-Host "CMake is already installed."
}

# Install Visual Studio Build Tools (including MSVC compiler)
if (-not (Test-Path "C:\Program Files (x86)\Microsoft Visual Studio\Installer")) {
    Write-Host "Installing Visual Studio Build Tools with C++ workload..."
    choco install visualstudio2022buildtools -y --install-arguments "--add Microsoft.VisualStudio.Workload.VCTools"
} else {
    Write-Host "Visual Studio Build Tools are already installed."
}

# Ensure MSVC compiler is added to PATH
$vcVarsPath = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if (Test-Path $vcVarsPath) {
    Write-Host "Adding MSVC compiler to PATH..."
    cmd /c "`"$vcVarsPath`""
} else {
    Write-Host "Error: Could not find vcvars64.bat. Please ensure Visual Studio Build Tools are installed."
    exit 1
}

# Activate the Anaconda environment
Write-Host "Activating Anaconda environment..."
conda activate jalising

# Install dependencies
Write-Host "Installing dependencies..."
pip install cmake

# Install dlib using pip
Write-Host "Installing dlib..."
pip install dlib --verbose

# If installation fails, try building from the GitHub source
if ($LASTEXITCODE -ne 0) {
    Write-Host "dlib installation failed. Attempting to build from source..."
    pip install git+https://github.com/davisking/dlib@v19.24 --verbose
} else {
    Write-Host "dlib installed successfully!"
}
