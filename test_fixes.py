import os
import sys
import tempfile
from Converter import generate_flowchart_direct, resource_path

# Test the resource path function
print("Testing resource path function:")
print(f"Current directory: {os.getcwd()}")
print(f"Script location: {os.path.abspath(__file__)}")

# Test font path
font_path = resource_path("fonts/NotoSans-Regular.ttf")
print(f"Font path: {font_path}")
print(f"Font exists: {os.path.exists(font_path)}")

# Test with sample pseudocode
sample_code = """START
INPUT x
IF x > 0 THEN
OUTPUT "Positive"
ELSE
OUTPUT "Not positive"
ENDIF
STOP"""

# Create temporary files
temp_dir = tempfile.gettempdir()
temp_input = os.path.join(temp_dir, "test_input.txt")
temp_output = os.path.join(temp_dir, "test_output.png")

print(f"\nTesting with temporary files:")
print(f"Input file: {temp_input}")
print(f"Output file: {temp_output}")

try:
    # Write test code to temp file
    with open(temp_input, 'w', encoding='utf-8') as f:
        f.write(sample_code)
    
    # Try to generate flowchart
    generate_flowchart_direct(12, temp_input, temp_output, font_path)
    
    print(f"\nSuccess! Generated flowchart at: {temp_output}")
    print(f"Output file exists: {os.path.exists(temp_output)}")
    
    # Clean up
    if os.path.exists(temp_input):
        os.remove(temp_input)
    if os.path.exists(temp_output):
        os.remove(temp_output)
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
