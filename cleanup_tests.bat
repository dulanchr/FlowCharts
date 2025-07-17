@echo off
echo ==========================================
echo   Cleaning up unnecessary files...
echo ==========================================

REM Remove test and debug files
echo Removing test and debug files...
if exist debug_font.py del debug_font.py
if exist debug_step_by_step.py del debug_step_by_step.py
if exist test_flask_endpoint.py del test_flask_endpoint.py
if exist test_simple.py del test_simple.py
if exist test_page.html del test_page.html
if exist test_fixes.py del test_fixes.py

REM Remove desktop application files
echo Removing desktop application files...
if exist flowchart_gui.py del flowchart_gui.py
if exist flowchart_gui.spec del flowchart_gui.spec
if exist run_flowchart_generator.bat del run_flowchart_generator.bat
if exist test_executable.bat del test_executable.bat
if exist build_exe.bat del build_exe.bat
if exist icon.ico del icon.ico
if exist version_info.txt del version_info.txt
if exist requirements.txt del requirements.txt

REM Remove temporary files
echo Removing temporary files...
if exist enter.png del enter.png
if exist enter.txt del enter.txt
if exist temp_flowchart.png del temp_flowchart.png

REM Remove old documentation
echo Removing old documentation...
if exist BUILD_INSTRUCTIONS.md del BUILD_INSTRUCTIONS.md
if exist FIXES_APPLIED.md del FIXES_APPLIED.md
if exist FONT_CHANGES.md del FONT_CHANGES.md
if exist GUI_IMPROVEMENTS.md del GUI_IMPROVEMENTS.md

REM Remove build artifacts
echo Removing build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo ==========================================
echo   Cleanup completed!
echo ==========================================
echo.
echo Files removed:
echo - Test and debug files
echo - Desktop application files
echo - Build artifacts
echo - Temporary files
echo - Old documentation
echo.
echo Essential web app files preserved:
echo ✓ app.py (main Flask application)
echo ✓ Converter.py (core logic)
echo ✓ tree.py (tree utilities)
echo ✓ templates/ (web interface)
echo ✓ fonts/ (font files)
echo ✓ web_requirements.txt (dependencies)
echo ✓ Startup scripts (*.bat)
echo ✓ Documentation (README_WEB.md, etc.)
echo ✓ Docker files
echo ✓ verify_app.py
echo.
echo Your web application is ready to use!
echo Run: python app.py or run_web_app.bat
echo.
pause
