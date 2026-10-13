@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo   Medien-Sortierer - Windows-EXE bauen (PyInstaller)
echo ============================================================
echo.

REM --- Python finden (py-Launcher bevorzugt) ---
set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo [FEHLER] Python wurde nicht gefunden.
    echo Installiere Python von https://www.python.org/downloads/
    echo und aktiviere beim Setup "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo Python-Aufruf: %PY%
%PY% --version
echo.

REM --- 1) Eingabedatei abfragen ---
:ask_script
set "SCRIPT="
set /p "SCRIPT=Welche Datei soll umgewandelt werden? [main.py]: "
if not defined SCRIPT set "SCRIPT=main.py"
if not exist "%SCRIPT%" (
    echo [FEHLER] Datei "%SCRIPT%" nicht gefunden. Bitte erneut eingeben.
    echo.
    goto ask_script
)

REM --- 2) Namen der EXE abfragen ---
set "APPNAME="
set /p "APPNAME=Wie soll die EXE heissen? [MedienSortierer]: "
if not defined APPNAME set "APPNAME=MedienSortierer"
if /i "%APPNAME:~-4%"==".exe" set "APPNAME=%APPNAME:~0,-4%"

echo.
echo ------------------------------------------------------------
echo   Eingabedatei : %SCRIPT%
echo   EXE-Name     : %APPNAME%.exe
echo   Modus        : --onefile --windowed
echo ------------------------------------------------------------
echo.
set "OK="
set /p "OK=Starten? [J/n]: "
if /i "%OK%"=="n" (
    echo Abgebrochen.
    pause
    exit /b 0
)

REM --- PyInstaller sicherstellen ---
%PY% -m PyInstaller --version >nul 2>nul
if errorlevel 1 (
    echo PyInstaller wird installiert ...
    %PY% -m pip install --upgrade pip pyinstaller
    if errorlevel 1 (
        echo [FEHLER] Installation von PyInstaller fehlgeschlagen.
        pause
        exit /b 1
    )
)

REM --- Bauen ---
echo.
echo Baue %APPNAME%.exe ...
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name "%APPNAME%" "%SCRIPT%"
if errorlevel 1 (
    echo.
    echo [FEHLER] Der Build ist fehlgeschlagen. Siehe Ausgabe oben.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Fertig:  dist\%APPNAME%.exe
echo ============================================================
echo.
pause
endlocal
