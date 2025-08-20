@echo off
setlocal EnableDelayedExpansion

:: Title and heading
color 03
echo ===============================================
echo           AUTO SWITCH PANEL ENV SETUP          
echo ===============================================
echo.
echo After continue, this bat file will:
echo 1. setup anaconda env named `switch`.
echo 2. git clone repo into current folder.
echo 3. pip install modules, to the env.
echo.
color 07

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
    CALL conda create -y -n switch python=3.10
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

:: Clone 'tomography'
echo.
echo [INFO] Repository: tomography
if exist tomography (
    echo [INFO] 'tomography' folder exists.

    :ask_tomo
    set /p USER_CHOICE="Do you want to (K)eep or (O)verwrite it? [K/O]: "
    set "USER_CHOICE=!USER_CHOICE: =!"
    if /i "!USER_CHOICE!"=="K" (
        echo [INFO] Keeping existing folder.
    ) else if /i "!USER_CHOICE!"=="O" (
        echo [INFO] Overwriting 'tomography'...
        rmdir /s /q tomography
        git clone https://github.com/ElenBOT/tomography
    ) else (
        echo [WARNING] Invalid choice. Please enter K or O.
        goto ask_tomo
    )
) else (
    echo [INFO] Cloning 'tomography'...
    git clone https://github.com/ElenBOT/tomography
)

:: Clone 'ats9371_for_tomography'
echo.
echo [INFO] Repository: ats9371_for_tomography
if exist ats9371_for_tomography (
    echo [INFO] 'ats9371_for_tomography' folder exists.

    :ask_ats
    set /p USER_CHOICE="Do you want to (K)eep or (O)verwrite it? [K/O]: "
    set "USER_CHOICE=!USER_CHOICE: =!"
    if /i "!USER_CHOICE!"=="K" (
        echo [INFO] Keeping existing folder.
    ) else if /i "!USER_CHOICE!"=="O" (
        echo [INFO] Overwriting 'ats9371_for_tomography'...
        rmdir /s /q ats9371_for_tomography
        git clone https://github.com/ElenBOT/ats9371_for_tomography
    ) else (
        echo [WARNING] Invalid choice. Please enter K or O.
        goto ask_ats
    )
) else (
    echo [INFO] Cloning 'ats9371_for_tomography'...
    git clone https://github.com/ElenBOT/ats9371_for_tomography
)


:: Install packages for 'tomography'
echo.
echo [INFO] Installing Python packages for 'tomography'...
pushd tomography
if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        color 0E
        echo [WARNING] Some packages may have failed to install in 'tomography'.
    ) else (
        echo [INFO] Packages installed successfully for 'tomography'.
    )
) else (
    echo [WARNING] requirements.txt not found in 'tomography', skipping...
)
popd

:: Install packages for 'ats9371_for_tomography'
echo [INFO] Installing Python packages for 'ats9371_for_tomography'...
pushd ats9371_for_tomography
if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        color 0E
        echo [WARNING] Some packages may have failed to install in 'ats9371_for_tomography'.
    ) else (
        echo [INFO] Packages installed successfully for 'ats9371_for_tomography'.
    )
) else (
    echo [WARNING] requirements.txt not found in 'ats9371_for_tomography', skipping...
)
popd


echo.
echo ==================================================
echo           SETUP COMPLETE - READY TO USE           
echo ==================================================
color 0A
endlocal
pause