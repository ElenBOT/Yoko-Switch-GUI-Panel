@echo off
setlocal EnableDelayedExpansion

:: Title and heading
color 03
echo ===============================================
echo           AUTO SWITCH PANEL ENV SETUP          
echo ===============================================
echo.


:: Conda detection
set "CONDA_ANACONDA=%USERPROFILE%\anaconda3"
set "CONDA_MINICONDA=%USERPROFILE%\miniconda3"
set "CONDA_PROGDATA=C:\ProgramData\Anaconda3"
set "CONDA_ROOT="

if exist "%CONDA_ANACONDA%" (
    set "CONDA_ROOT=%CONDA_ANACONDA%"
) else if exist "%CONDA_MINICONDA%" (
    set "CONDA_ROOT=%CONDA_MINICONDA%"
) else if exist "%CONDA_PROGDATA%" (
    set "CONDA_ROOT=%CONDA_PROGDATA%"
)

if defined CONDA_ROOT (
    echo [INFO] Found Conda at: %CONDA_ROOT%
) else (
    color 0C
    echo [ERROR] Conda installation not found!
    pause
    exit /b
)

:: Check if setup was already done
if exist "setup_complete.txt" (
    echo [INFO] Setup already completed.
    echo [INFO] Activating conda env and launching app...

    :: Current directory
    echo.
    echo [INFO] Current directory: %cd%
    echo.

    :: Initialize Conda
    echo [INFO] activate env ...
    CALL "%CONDA_ROOT%\condabin\conda.bat" activate switch

    :: Open Streamlit app
    echo [INFO] Launching GUI...
    cd "Yoko-Switch-GUI-Panel"
    python -m streamlit run app.py
    endlocal
    exit /b
)

:: ---------------------------
:: FIRST RUN: Full setup
:: ---------------------------

echo This bat file will:
echo 1. setup anaconda env named `switch`.
echo 2. git clone repo into current folder.
echo 3. pip install modules to the env.
echo.
color 07



:: Current directory
echo.
echo [INFO] Current directory: %cd%
echo.

:: Initialize Conda
echo [INFO] Initializing Conda...
CALL "%CONDA_ROOT%\condabin\conda.bat" activate base

:: Check or create environment
echo.
echo [INFO] Checking Conda environment 'switch'...
conda env list | findstr "switch" >nul
if errorlevel 1 (
    echo [INFO] Creating new environment 'switch'...
    CALL conda create -y -n switch python=3.11
    if errorlevel 1 (
        color 0C
        echo [ERROR] Failed to create environment!
        pause
        exit /b
    )
) else (
    echo [INFO] Environment 'switch' already exists.
)

:: Activate environment
color 07
echo [INFO] Activating 'switch'...
CALL conda activate switch
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to activate environment!
    pause
    exit /b
)

:: Git check
echo.
echo [INFO] Checking for Git...
where git >nul 2>nul
if errorlevel 1 (
    color 0C
    echo [ERROR] Git is not installed or not in PATH.
    pause
    exit /b
) else (
    echo [INFO] Git is available.
)

:: Clone repo
echo.
echo [INFO] Cloning repo...
git clone https://github.com/ElenBOT/Yoko-Switch-GUI-Panel
cd "Yoko-Switch-GUI-Panel"
del /f /q auto_setup.bat
cd ..

:: Install packages
echo.
echo [INFO] Installing Python packages 
pip install numpy streamlit pyvisa

:: Write setup complete marker
echo %date% %time% > setup_complete.txt

echo.
echo ==================================================
echo           SETUP COMPLETE - READY TO USE           
echo ==================================================
color 0A
endlocal
pause
