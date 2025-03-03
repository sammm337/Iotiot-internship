import logging
import os
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(bot_name):
    # Get the base directory (parent of Bots folder)
    base_dir = Path(__file__).resolve().parent.parent
    logs_dir = base_dir / "Logs"
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create a logger
    logger = logging.getLogger(bot_name)
    
    # Only add handlers if the logger doesn't have any
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create a file handler for the combined log file with UTF-8 encoding
        log_filename = logs_dir / "hr_verification.log"
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Create console handler with UTF-8 encoding for Windows
        if sys.platform == 'win32':
            # Use sys.stdout with UTF-8 encoding for Windows
            console_handler = logging.StreamHandler(sys.stdout)
        else:
            console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter with bot name included
        formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger 