#!/usr/bin/env python3
"""
Deep Space Dominator 3000
Main entry point for the application
"""

import os
import sys
import webbrowser
import threading
import time
from backend.app import app

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')
    webbrowser.open('http://localhost:5500/frontend/index.html')

def start_frontend():
    """Start a simple HTTP server for frontend"""
    os.system('cd frontend && python -m http.server 5500')

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     Deep Space Dominator 3000 - Cosmic Signal Analyzer   ║
    ╚════════════════════════════════════════════════════════════╝
    
    Starting systems...
    """)
    
    # Start frontend server in a separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Open browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start backend server
    print("✅ Backend server starting on http://localhost:5000")
    print("✅ Frontend server starting on http://localhost:5500")
    print("\nPress Ctrl+C to stop all servers\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Deep Space Dominator 3000...")
        sys.exit(0)
