from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import tempfile
import base64
import signal
import time
from io import BytesIO
from PIL import Image
from Converter import generate_flowchart_direct
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def resource_path(relative_path):
    """ Get absolute path to resource """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_flowchart', methods=['POST'])
def generate_flowchart():
    try:
        logger.info("Received flowchart generation request")
        data = request.get_json()
        pseudocode = data.get('pseudocode', '').strip()
        font_size = int(data.get('font_size', 20))
        
        logger.info(f"Pseudocode length: {len(pseudocode)}, Font size: {font_size}")
        
        if not pseudocode:
            return jsonify({'error': 'Please enter some pseudocode'}), 400
        
        # Create temporary files
        temp_dir = tempfile.gettempdir()
        temp_input = os.path.join(temp_dir, f"temp_input_{os.getpid()}.txt")
        temp_output = os.path.join(temp_dir, f"temp_output_{os.getpid()}.png")
        
        logger.info(f"Temp input: {temp_input}")
        logger.info(f"Temp output: {temp_output}")
        
        try:
            # Write pseudocode to temporary file
            with open(temp_input, 'w', encoding='utf-8') as f:
                f.write(pseudocode)
            
            logger.info("Pseudocode written to temp file")
            
            # Set font path
            font_path = resource_path("fonts/NotoSans-Regular.ttf")
            if not os.path.exists(font_path):
                font_path = resource_path("fonts/SFUIText-Regular.otf")
            
            logger.info(f"Using font: {font_path}")
            logger.info(f"Font exists: {os.path.exists(font_path)}")
            
            # Check if font exists
            if not os.path.exists(font_path):
                return jsonify({'error': f'Font file not found: {font_path}'}), 500
            
            # Set up timeout for flowchart generation (30 seconds)
            if hasattr(signal, 'SIGALRM'):  # Unix only
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(30)
            
            try:
                # Generate flowchart
                logger.info("Starting flowchart generation...")
                generate_flowchart_direct(font_size, temp_input, temp_output, font_path)
                logger.info("Flowchart generation completed")
                
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)  # Cancel alarm
                    
            except TimeoutException:
                return jsonify({'error': 'Flowchart generation timed out. Please try with simpler pseudocode.'}), 500
            
            # Check if output was created
            if not os.path.exists(temp_output):
                return jsonify({'error': 'Flowchart generation failed - no output file created'}), 500
            
            logger.info(f"Output file created, size: {os.path.getsize(temp_output)} bytes")
            
            # Convert image to base64
            with open(temp_output, 'rb') as f:
                img_data = f.read()
                img_base64 = base64.b64encode(img_data).decode()
            
            logger.info("Image converted to base64")
            
            return jsonify({
                'success': True,
                'image': f'data:image/png;base64,{img_base64}'
            })
            
        except Exception as e:
            logger.error(f"Error in flowchart generation: {str(e)}")
            return jsonify({'error': f'Error generating flowchart: {str(e)}'}), 500
            
        finally:
            # Clean up temporary files
            for temp_file in [temp_input, temp_output]:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                        logger.info(f"Cleaned up: {temp_file}")
                    except:
                        pass
                        
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/load_example')
def load_example():
    example_code = """INPUT age
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
ENDIF"""
    return jsonify({'pseudocode': example_code})

@app.route('/download_flowchart', methods=['POST'])
def download_flowchart():
    try:
        data = request.get_json()
        pseudocode = data.get('pseudocode', '').strip()
        font_size = int(data.get('font_size', 20))
        
        if not pseudocode:
            return jsonify({'error': 'Please enter some pseudocode'}), 400
        
        # Create temporary files
        temp_dir = tempfile.gettempdir()
        temp_input = os.path.join(temp_dir, f"temp_input_{os.getpid()}.txt")
        temp_output = os.path.join(temp_dir, f"flowchart_{os.getpid()}.png")
        
        try:
            # Write pseudocode to temporary file
            with open(temp_input, 'w', encoding='utf-8') as f:
                f.write(pseudocode)
            
            # Set font path
            font_path = resource_path("fonts/NotoSans-Regular.ttf")
            if not os.path.exists(font_path):
                font_path = resource_path("fonts/SFUIText-Regular.otf")
            
            # Generate flowchart
            generate_flowchart_direct(font_size, temp_input, temp_output, font_path)
            
            # Return file for download
            return send_file(temp_output, as_attachment=True, download_name='flowchart.png')
            
        except Exception as e:
            return jsonify({'error': f'Error generating flowchart: {str(e)}'}), 500
            
        finally:
            # Clean up input file
            if os.path.exists(temp_input):
                try:
                    os.remove(temp_input)
                except:
                    pass
                    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
