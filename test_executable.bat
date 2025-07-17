@echo off
echo Testing the fixed FlowchartGenerator.exe...
echo.

cd /d "d:\ICTDulanChathuranga\FlowCharts\dist"

REM Test if the executable exists
if not exist FlowchartGenerator.exe (
    echo ERROR: FlowchartGenerator.exe not found!
    pause
    exit /b 1
)

echo Starting FlowchartGenerator.exe in background...
start "" FlowchartGenerator.exe

echo.
echo The application should now be running without the previous error.
echo If you see the GUI window, the fix was successful!
echo.
pause
