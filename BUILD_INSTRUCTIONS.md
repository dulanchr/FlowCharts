# Flowchart Generator - Executable Build

This guide explains how to create an executable file from the Flowchart Generator application.

## Prerequisites

- Python 3.6 or higher installed
- pip package manager

## Building the Executable

### Method 1: Using the Build Script (Recommended)

1. Double-click `build_exe.bat` to run the build script
2. The script will:
   - Install required packages
   - Create the executable using PyInstaller
   - Place the executable in the `dist` folder

### Method 2: Manual Build

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Build the executable:
   ```
   pyinstaller flowchart_gui.spec
   ```

## Files Created

After building, you'll find:
- `dist/FlowchartGenerator.exe` - The main executable file
- `build/` - Temporary build files (can be deleted)

## Running the Executable

1. Navigate to the `dist` folder
2. Double-click `FlowchartGenerator.exe` to run the application
3. The executable is standalone and includes all necessary dependencies

## Distribution

The executable in the `dist` folder can be distributed to other Windows computers without requiring Python to be installed on the target machine.

## File Structure

- `flowchart_gui.py` - Main GUI application
- `Converter.py` - Core flowchart generation logic
- `tree.py` - Tree structure utilities
- `fonts/` - Font files (included in executable)
- `icon.ico` - Application icon
- `requirements.txt` - Python dependencies
- `flowchart_gui.spec` - PyInstaller configuration
- `version_info.txt` - Version information for the executable
- `build_exe.bat` - Build script

## Troubleshooting

If the build fails:
1. Ensure all Python dependencies are installed
2. Check that all required files are present
3. Run the build command manually to see detailed error messages
4. Make sure the fonts folder and icon.ico are in the correct location

## Notes

- The executable includes all fonts and dependencies
- The application icon is embedded in the executable
- The executable is created as a Windows GUI application (no console window)
- File size will be larger than the source code due to included Python runtime
