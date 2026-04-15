import logging
import os


class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLORS = {
        logging.DEBUG: "\033[90m",
        logging.INFO: "\033[35m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[1;91m"
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)

        levelname = f"{color}{record.levelname}{self.RESET}"

        # THIS is key
        # location = f"{record.pathname}:{record.lineno}"
        
        
        filename = os.path.basename(record.pathname)
        location = f"{color}{filename}:{record.lineno}{self.RESET}"

        message = record.getMessage()

        return f"[{levelname}] {location} | {message}"


def setup_logging(level: int = logging.INFO):
    """
    Configure root logger (call once in main).
    """

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter())

    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get module-specific logger.
    """
    return logging.getLogger(name)