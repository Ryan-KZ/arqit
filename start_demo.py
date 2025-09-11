#!/usr/bin/env python3
"""
Global Customer Support Demo Launcher
Starts both the Flask API server and provides instructions for the React frontend.
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check if uv is available
    try:
        subprocess.run(['uv', '--version'], capture_output=True, check=True)
        print("✓ uv package manager found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv package manager not found. Please install uv first.")
        return False
    
    # Check if npm is available
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
        print("✓ npm found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js and npm first.")
        return False
    
    return True

def setup_backend():
    """Set up and sync backend dependencies."""
    print("🐍 Setting up Python backend...")
    try:
        subprocess.run(['uv', 'sync'], check=True, cwd='.')
        print("✓ Backend dependencies synced")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to sync backend dependencies: {e}")
        return False

def setup_frontend():
    """Set up frontend dependencies if not already done."""
    frontend_dir = Path('./frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    node_modules = frontend_dir / 'node_modules'
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], check=True, cwd=frontend_dir)
            print("✓ Frontend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
    else:
        print("✓ Frontend dependencies already installed")
    
    return True

def start_backend():
    """Start the Flask API server."""
    print("🚀 Starting Flask API server...")
    try:
        subprocess.run(['uv', 'run', 'api_server.py'], cwd='.')
    except KeyboardInterrupt:
        print("\n🛑 API server stopped")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")

def print_instructions():
    """Print instructions for starting the frontend."""
    print("\n" + "="*60)
    print("🌍 GLOBAL CUSTOMER SUPPORT DEMO")
    print("="*60)
    print("\n📋 Backend API Server:")
    print("   • Status: Running on http://localhost:5001")
    print("   • US Agent: http://20.185.179.136:61100/v1") 
    print("   • EU Agent: http://9.163.149.120:61102/v1")
    
    print("\n🌐 Frontend React App:")
    print("   • Open a NEW terminal window")
    print("   • Run these commands:")
    print("     cd frontend")
    print("     npm start")
    print("   • Open http://localhost:3000 in your browser")
    
    print("\n📖 Demo Flow:")
    print("   1. Select a customer and submit a support query")
    print("   2. Watch real-time agent collaboration")  
    print("   3. View the personalized response")
    
    print("\n🔧 Features:")
    print("   • Multi-region agent collaboration (US ↔ EU)")
    print("   • GDPR-compliant data handling")
    print("   • Personalized customer responses")
    print("   • Real-time collaboration visualization")
    
    print("\n🛑 To stop: Press Ctrl+C in this terminal")
    print("="*60)

def main():
    """Main demo launcher."""
    print("🎯 Global Customer Support Demo Launcher")
    print("-" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("⚠️  Frontend setup failed, but you can set it up manually")
    
    # Print instructions
    print_instructions()
    
    # Start backend server
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped. Thanks for trying the Global Customer Support Demo!")

if __name__ == "__main__":
    main()