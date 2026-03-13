import logging
import sys

fromconfig.environment import environment


def _resolve_log_level(level_name: str) -> int:
    level = getattr(logging, level_name.upper(), None)
    return level if isinstance(level, int) else logging.INFO

def setup_logger(name: str = "AegisSwarm", level: int = logging.INFO) -> logging.Logger:
    """Sets up a structured logger for the application."""
    logger = logging.getLogger(name)
    effective_level = _resolve_log_level(environment.LOG_LEVEL) if level == logging.INFO else level
    logger.setLevel(effective_level)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(effective_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)

    logger.propagate = False
        
    return logger

# Default logger instance
logger = setup_logger()
