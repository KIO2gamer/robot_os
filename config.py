# config.py
"""
Configuration module for Robot OS.
Centralized place for GPIO pins, database paths, and operating modes.
"""

import logging
from logging.handlers import RotatingFileHandler

# ============ GPIO PIN CONFIGURATION ============
GPIO_CONFIG = {
    "LEFT_MOTOR": {
        "forward": 17,
        "backward": 27,
        "enable": 12,
    },
    "RIGHT_MOTOR": {
        "forward": 22,
        "backward": 23,
        "enable": 13,
    },
}

# ============ DATABASE CONFIGURATION ============
DB_CONFIG = {
    "db_name": "vending_data.db",
    "timeout": 5.0,  # Connection timeout in seconds
}

# ============ OPERATING MODES ============
class OperatingMode:
    """Operating modes for the robot system."""
    MANUAL = "manual"          # User controls via UI
    AUTONOMOUS = "autonomous"  # Vision-guided navigation
    DEMO = "demo"              # Pre-programmed demo scenario


DEFAULT_MODE = OperatingMode.MANUAL

# ============ MOTION PARAMETERS ============
MOTION = {
    "default_speed": 0.8,
    "turn_speed": 0.6,
    "emergency_stop_timeout": 0.5,  # seconds
}

# ============ LOGGING CONFIGURATION ============
def setup_logging(log_file="robot_os.log", log_level=logging.INFO):
    """Initialize logging with file and console handlers."""
    logger = logging.getLogger("RobotOS")
    logger.setLevel(log_level)
    if logger.handlers:
        return logger
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
    )
    file_handler.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logging()
