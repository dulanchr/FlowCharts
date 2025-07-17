#!/usr/bin/env python3
"""
Final verification script for the web application
"""
import os
import sys

def verify_application():
    """Verify all components are working"""
    print("🔍 Verifying Web Application Components...")
    print("=" * 50)
    
    # Check 1: Core files exist
    required_files = [
        'app.py',
        'Converter.py', 
        'tree.py',
        'templates/index.html',
        'fonts/NotoSans-Regular.ttf',
        'web_requirements.txt'
    ]
    
    print("\n1. Checking required files...")
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            return False
    
    # Check 2: Test imports
    print("\n2. Testing imports...")
    try:
        from Converter import generate_flowchart_direct
        print("   ✅ Converter module")
    except Exception as e:
        print(f"   ❌ Converter import failed: {e}")
        return False
    
    try:
        from app import app
        print("   ✅ Flask app")
    except Exception as e:
        print(f"   ❌ Flask app import failed: {e}")
        return False
    
    # Check 3: Test Flask routes
    print("\n3. Testing Flask routes...")
    try:
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("   ✅ Home page route")
            else:
                print(f"   ❌ Home page failed: {response.status_code}")
                return False
                
            response = client.get('/load_example')
            if response.status_code == 200:
                print("   ✅ Load example route")
            else:
                print(f"   ❌ Load example failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"   ❌ Flask route test failed: {e}")
        return False
    
    # Check 4: Test core functionality
    print("\n4. Testing core functionality...")
    try:
        import tempfile
        
        test_code = "START\nINPUT x\nOUTPUT x\nSTOP"
        temp_dir = tempfile.gettempdir()
        temp_input = os.path.join(temp_dir, "verify_input.txt")
        temp_output = os.path.join(temp_dir, "verify_output.png")
        
        with open(temp_input, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        font_path = "fonts/NotoSans-Regular.ttf"
        if not os.path.exists(font_path):
            font_path = "fonts/SFUIText-Regular.otf"
        
        generate_flowchart_direct(20, temp_input, temp_output, font_path)
        
        if os.path.exists(temp_output):
            print("   ✅ Flowchart generation")
            # Cleanup
            os.remove(temp_input)
            os.remove(temp_output)
        else:
            print("   ❌ Flowchart generation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Core functionality test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL VERIFICATIONS PASSED!")
    print("\n✨ Your web application is ready to use!")
    print("\n🚀 To start the application:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Or use: run_web_app.bat")
    print("\n📚 Documentation:")
    print("   - README_WEB.md - Usage instructions")
    print("   - TROUBLESHOOTING.md - Help guide")
    print("   - DEPLOYMENT_GUIDE.md - Deployment options")
    
    return True

if __name__ == "__main__":
    success = verify_application()
    if not success:
        print("\n❌ Some verifications failed. Please check the issues above.")
        sys.exit(1)
    else:
        print("\n✅ Web application verification complete!")
        
    input("\nPress Enter to exit...")
