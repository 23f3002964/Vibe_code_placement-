#!/usr/bin/env python3
"""
Script to run the Flask application
"""

import subprocess
import sys
import os

def run_app():
    print("Starting the Placement Portal Flask Application...")
    
    # Set environment variables
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    # Run the Flask application
    try:
        result = subprocess.run([sys.executable, '-m', 'flask', 'run'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    run_app()