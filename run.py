#!/usr/bin/env python3
"""
Run script for SkillSwap Flask application
"""

from app import app

if __name__ == '__main__':
    print("Starting SkillSwap application...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 