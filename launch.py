# launch.py
import os
import threading
import time
import webbrowser
import sys

def run_backend():
    """Run the Flask backend"""
    # Get the absolute path to the backend folder
    backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    os.chdir(backend_path)
    print(f"📡 Starting backend in: {backend_path}")
    # Use python -m to run as module
    os.system('python -m app')
    # Note: We don't chdir back because this runs in a separate thread

def run_frontend():
    """Run the frontend HTTP server"""
    time.sleep(2)  # Wait for backend to start
    # Get the absolute path to the frontend folder
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    os.chdir(frontend_path)
    print(f"🖥️ Starting frontend in: {frontend_path}")
    os.system('python -m http.server 5500')

def open_browser():
    """Open browser after servers start"""
    time.sleep(3)
    print("\n🌐 Opening browser...")
    webbrowser.open('http://localhost:5500/index.html')
    webbrowser.open('http://localhost:5000/api/status')

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║     Deep Space Dominator 3000 - Cosmic Signal Analyzer   ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("🚀 Starting servers...")
    
    # Start backend in a thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Start frontend in a thread
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("✅ Backend: http://localhost:5000")
    print("✅ Frontend: http://localhost:5500")
    print("\n⚠️  Press Ctrl+C to stop all servers\n")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        # Kill all Python processes (Windows)
        if sys.platform == "win32":
            os.system('taskkill /f /im python.exe 2>nul')
        sys.exit(0)
