#!/usr/bin/env python3
"""
Quick start script for the Football Statistics Web Application
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'player_statistics.csv',
        'player_performance_model.pkl'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("\n" + "=" * 60)
        print("⚠️  Missing Required Files")
        print("=" * 60)
        print("\nThe following files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n🔧 Solution: Run the training script first")
        print("\n   python train_model.py\n")
        print("=" * 60)
        return False
    
    return True


def main():
    print("\n" + "=" * 60)
    print("⚽ Football Player Statistics Web Application")
    print("=" * 60)
    
    # Check if data and model exist
    if not check_requirements():
        print("\n❌ Cannot start the website. Please run train_model.py first.\n")
        sys.exit(1)
    
    # Start Flask app
    print("\n✅ All required files found!")
    print("\n🚀 Starting web server...")
    print("\n📱 Open your browser and visit:")
    print("   http://localhost:8080")
    print("\n⏸️  Press CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

