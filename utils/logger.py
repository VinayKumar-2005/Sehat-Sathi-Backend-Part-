import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configure Logger
    logger = logging.getLogger('SehatSaathi')
    logger.setLevel(logging.INFO)

    # File Handler (Writes to file, max 1MB size, keeps 10 backups)
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=1024*1024, backupCount=10)
    
    # Format: [Time] [Level] Message [Location]
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        
    return logger

# Global logger instance
app_logger = setup_logger()