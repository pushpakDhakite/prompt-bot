"""
Launcher script for the AI Prompt Generator GUI application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from prompt_generator import main
    
    if __name__ == '__main__':
        print("Starting AI Prompt Generator Pro...")
        main()
        
except ImportError as e:
    print(f"Error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Failed to start application: {e}")
    sys.exit(1)