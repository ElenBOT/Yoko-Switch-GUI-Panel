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
    echo [ERROR] Conda installation not found!
    pause
    exit /b
)

:: Current directory
echo.
echo [INFO] Current directory: %cd%
echo.

:: activate conda env
echo [INFO] activate conda env
CALL "%CONDA_ROOT%\condabin\conda.bat" activate switch

:: open app
python -m streamlit run app.py