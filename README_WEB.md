# Flowchart Web Application

A web-based version of the Pseudocode to Flowchart Converter that converts pseudocode into beautiful flowcharts instantly.

## Features

- **Web Interface**: Clean, modern Bootstrap-based interface
- **Real-time Generation**: Generate flowcharts instantly from pseudocode
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Zoom Controls**: Zoom in/out to view flowcharts at different scales
- **Download Support**: Download generated flowcharts as PNG images
- **Example Code**: Load example pseudocode to get started quickly
- **Fullscreen Mode**: View flowcharts in fullscreen for better visualization

## Quick Start

### Method 1: Using the Batch File (Recommended)
1. Double-click `run_web_app.bat`
2. The script will automatically:
   - Create a virtual environment
   - Install required packages
   - Start the web server
3. Open your browser and go to `http://localhost:5000`

### Method 2: Manual Setup
1. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

3. Install requirements:
   ```cmd
   pip install -r web_requirements.txt
   ```

4. Run the application:
   ```cmd
   python app.py
   ```

5. Open your browser and go to `http://localhost:5000`

## Usage

1. **Enter Pseudocode**: Type or paste your pseudocode in the left panel
2. **Adjust Font Size**: Use the font size control to set the desired size (8-40)
3. **Generate Flowchart**: Click "Generate Flowchart" to create your flowchart
4. **View Results**: The flowchart will appear in the right panel
5. **Download**: Click "Download PNG" to save the flowchart to your computer

## Pseudocode Syntax

The application supports the following pseudocode constructs:

### Basic Statements
- `START` - Start of the program
- `STOP` - End of the program
- `INPUT variable` - Input operation
- `OUTPUT expression` - Output operation
- `variable = expression` - Assignment

### Control Structures
- `IF condition THEN ... ELSE ... ENDIF` - Conditional statements
- `WHILE condition DO ... ENDWHILE` - While loops
- `FOR variable <- start TO end ... NEXT variable` - For loops (converted to while)

### Example Pseudocode
```
INPUT age
IF age >= 18 THEN
    IF age < 35 THEN
        OUTPUT "Associate"
    ELSE 
        IF age <= 55 THEN
            OUTPUT "Management"
        ELSE 
            OUTPUT "Too old"  
        ENDIF
    ENDIF
ELSE
    OUTPUT "Too young"
ENDIF
```

## File Structure

```
FlowCharts WEB/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Web interface template
├── Converter.py           # Core conversion logic (unchanged)
├── tree.py               # Tree utilities (unchanged)
├── fonts/                # Font files
│   ├── NotoSans-Regular.ttf
│   └── SFUIText-Regular.otf
├── web_requirements.txt   # Python dependencies for web app
├── run_web_app.bat       # Quick start batch file
├── start_menu.bat        # Interactive startup menu
├── quick_fix.bat         # System diagnostics and fixes
├── TROUBLESHOOTING.md    # Troubleshooting guide
├── DEPLOYMENT_GUIDE.md   # Deployment instructions
└── README_WEB.md         # This file
```

## API Endpoints

### POST /generate_flowchart
Generate a flowchart from pseudocode.

**Request Body:**
```json
{
    "pseudocode": "INPUT x\nOUTPUT x",
    "font_size": 20
}
```

**Response:**
```json
{
    "success": true,
    "image": "data:image/png;base64,..."
}
```

### GET /load_example
Load example pseudocode.

**Response:**
```json
{
    "pseudocode": "INPUT age\nIF age >= 18 THEN..."
}
```

### POST /download_flowchart
Download flowchart as PNG file.

**Request Body:**
```json
{
    "pseudocode": "INPUT x\nOUTPUT x",
    "font_size": 20
}
```

**Response:** PNG file download

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **"Python is not recognized"**
   - Ensure Python is installed and added to PATH
   - Download from https://python.org

2. **"pip is not recognized"**
   - Reinstall Python with "Add to PATH" option checked

3. **Port 5000 is already in use**
   - Change the port in `app.py` (line 120): `app.run(debug=True, host='0.0.0.0', port=5001)`

4. **Font not found errors**
   - Ensure the `fonts/` folder exists with the font files
   - Check that NotoSans-Regular.ttf or SFUIText-Regular.otf is present

### Development Mode

To run in development mode with auto-reload:
```cmd
set FLASK_ENV=development
python app.py
```

## Deployment

### Local Network Access
To make the application accessible from other devices on your network:
1. In `app.py`, change the host parameter: `app.run(debug=True, host='0.0.0.0', port=5000)`
2. Access via your computer's IP address: `http://YOUR_IP:5000`

### Production Deployment
For production deployment, consider using:
- **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **Docker**: Create a Dockerfile for containerized deployment
- **Cloud platforms**: Deploy to Heroku, AWS, or Azure

## License

This web application maintains the same license as the original desktop application.

## Contributing

Feel free to submit issues and pull requests to improve the web application.
