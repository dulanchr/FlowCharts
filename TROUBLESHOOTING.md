# Troubleshooting Guide for Flowchart Web Application

## Common Issues and Solutions

### Issue 1: Flowchart Generation Keeps Loading Forever

**Symptoms:**
- Clicking "Generate Flowchart" shows loading spinner
- Loading never completes
- No error message appears

**Possible Causes & Solutions:**

#### A. Font File Issues
```cmd
# Check if font files exist
dir fonts\
```
**Solution:** Make sure these files exist in the `fonts/` folder:
- `NotoSans-Regular.ttf`
- `SFUIText-Regular.otf`

#### B. Python Environment Issues
```cmd
# Test basic imports
python -c "import Converter; print('OK')"
python -c "import PIL; print('OK')"
python -c "import flask; print('OK')"
```
**Solution:** If any imports fail, reinstall requirements:
```cmd
pip install -r web_requirements.txt
```

#### C. Core Functionality Issues
```cmd
# Run the simple test
python test_simple.py
```
**Solution:** If the test fails, check error messages and fix accordingly.

### Issue 2: Server Not Starting

**Symptoms:**
- `python app.py` doesn't show any output
- Cannot access http://localhost:5000

**Solutions:**

#### A. Port Already in Use
```cmd
# Check what's using port 5000
netstat -ano | findstr :5000
```
**Solution:** Either kill the process or change port in app.py

#### B. Missing Dependencies
```cmd
# Install all requirements
pip install -r web_requirements.txt
```

#### C. Python Path Issues
```cmd
# Ensure Python is in PATH
python --version
```

### Issue 3: Font Loading Errors

**Symptoms:**
- Error message: "Font file not found"
- Generated flowchart has missing text

**Solutions:**

#### A. Copy Font Files
Make sure these files exist:
```
fonts/
├── NotoSans-Regular.ttf
└── SFUIText-Regular.otf
```

#### B. Check Font Permissions
```cmd
# Check if files are readable
dir fonts\ /A
```

### Issue 4: Memory or Performance Issues

**Symptoms:**
- Application becomes slow
- Generation takes very long
- System runs out of memory

**Solutions:**

#### A. Reduce Font Size
Try using smaller font sizes (8-16 instead of 20+)

#### B. Simplify Pseudocode
Test with simpler pseudocode first:
```
START
INPUT x
OUTPUT x
STOP
```

#### C. Clear Temporary Files
```cmd
# Clear temp directory
del /q %TEMP%\temp_*.txt
del /q %TEMP%\temp_*.png
```

### Issue 5: JavaScript Console Errors

**Symptoms:**
- Browser console shows errors
- Interface doesn't respond

**Solutions:**

#### A. Clear Browser Cache
- Press Ctrl+F5 to hard refresh
- Clear browser cache and cookies

#### B. Check Network Tab
- Open Developer Tools (F12)
- Check Network tab for failed requests

#### C. Disable Browser Extensions
- Try in incognito/private mode
- Disable ad blockers or script blockers

## Debugging Steps

### Step 1: Test Core Functionality
```cmd
python test_simple.py
```
This should show if the basic flowchart generation works.

### Step 2: Test Flask App
```cmd
python debug_run.bat
```
This will test core functionality and start the server with debug logging.

### Step 3: Test Browser Integration
1. Open http://localhost:5000/test
2. Try generating a simple flowchart
3. Check browser console for errors

### Step 4: Check Server Logs
When running `python app.py`, check console output for:
- "Received flowchart generation request"
- "Starting flowchart generation..."
- "Flowchart generation completed"

## Common Error Messages

### "Font file not found"
**Cause:** Missing font files
**Solution:** Copy font files to `fonts/` folder

### "Error generating flowchart: [PIL errors]"
**Cause:** Image processing issues
**Solution:** 
- Check if PIL/Pillow is installed correctly
- Try: `pip install Pillow --upgrade`

### "Server error: [import errors]"
**Cause:** Missing Python modules
**Solution:** `pip install -r web_requirements.txt`

### "Operation timed out"
**Cause:** Complex pseudocode taking too long
**Solution:** 
- Simplify pseudocode
- Reduce font size
- Check for infinite loops in pseudocode

## Manual Testing

### Test 1: Direct Function Call
```python
from Converter import generate_flowchart_direct
generate_flowchart_direct(20, "test.txt", "output.png", "fonts/NotoSans-Regular.ttf")
```

### Test 2: Flask Endpoint
```python
import json
from app import app

with app.test_client() as client:
    response = client.post('/generate_flowchart', 
                         json={'pseudocode': 'INPUT x\nOUTPUT x', 'font_size': 20})
    print(response.data)
```

### Test 3: Browser Testing
1. Open http://localhost:5000/test
2. Enter simple pseudocode
3. Check browser console for errors
4. Check network tab for request/response

## Getting Help

### Enable Debug Mode
In `app.py`, change the last line to:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Collect Information
When reporting issues, include:
1. Error messages from console
2. Browser console errors
3. Results from `python test_simple.py`
4. Python version: `python --version`
5. Operating system version

### Log Files
Check for log files in:
- Current directory: `app.log`
- Temp directory: `%TEMP%\flask_*.log`

## Alternative Solutions

### If Web App Doesn't Work
1. Use the original desktop application: `python flowchart_gui.py`
2. Use command line: `python Converter.py --code input.txt --output output.png`

### If Font Issues Persist
1. Download fonts from Google Fonts
2. Copy system fonts from Windows/Fonts folder
3. Use alternative font paths in code

### If Performance Issues Continue
1. Use smaller font sizes
2. Break complex pseudocode into smaller parts
3. Consider using the desktop version for complex flowcharts
