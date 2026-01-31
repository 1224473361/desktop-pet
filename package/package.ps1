Write-Host "Desktop Pet Packager"
Write-Host "=================="
Write-Host ""

# Set Python 3.12 path
$python_dir = "E:\install\python\python-3.12.0-embed-amd64"
$env:Path = "$python_dir;$env:Path"

# Variables
$src_dir = "../src"
$output_dir = "./dist"
$exe_name = "DesktopPet"

# Convert output directory to absolute path
$output_dir = Resolve-Path -Path $output_dir -ErrorAction SilentlyContinue
if (-not $output_dir) {
    $output_dir = Join-Path -Path $PSScriptRoot -ChildPath "dist"
}

# Create output directory
if (Test-Path $output_dir) {
    Remove-Item -Path $output_dir -Recurse -Force
}
New-Item -Path $output_dir -ItemType Directory -Force | Out-Null

# Check dependencies
Write-Host "Checking dependencies..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: PyInstaller not found!" -ForegroundColor Red
    Write-Host "Please run: pip install pyinstaller"
    exit 1
}

# Change to source directory
Push-Location -Path $src_dir

# Run PyInstaller
Write-Host ""
Write-Host "Running PyInstaller..."
Write-Host "This may take a few minutes..."

pyinstaller --name="$exe_name" --onefile --noconsole --distpath="$output_dir" --add-data="images/idle_animation;images/idle_animation" --add-data="images/click;images/click" --add-data="images/talk_background.jpg;images" --add-data="images/favicon.ico;images" --add-data="dialog/dialog.txt;dialog" --exclude-module="torch" --exclude-module="transformers" --exclude-module="numpy" --exclude-module="sympy" --exclude-module="pytorch" --hidden-import="PyQt6.QtCore" --hidden-import="PyQt6.QtGui" --hidden-import="PyQt6.QtWidgets" --hidden-import="PyQt6.sip" --hidden-import="PyQt6.Qt" main.py

$exit_code = $LASTEXITCODE

# Return to original directory
Pop-Location

# Check result
Write-Host ""
if ($exit_code -eq 0) {
    Write-Host "SUCCESS: Package created!" -ForegroundColor Green
    $exe_path = "$output_dir/$exe_name.exe"
    if (Test-Path $exe_path) {
        Write-Host "Executable: $exe_path" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Executable not found!" -ForegroundColor Red
    }
} else {
    Write-Host "ERROR: Packaging failed!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Done!"