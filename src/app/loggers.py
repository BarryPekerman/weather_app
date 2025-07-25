import logging
import os

# === Get logging level from environment ===
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# === Color Formatter for event logger ===
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m',
    }
    RESET = '\033[0m'

    def format(self, record):
        log_fmt = self.COLORS.get(record.levelname, self.RESET) + '[%(asctime)s] [%(levelname)s] %(message)s' + self.RESET
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# === Event Logger: console only, colored ===
event_logger = logging.getLogger("event_logger")
event_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

if not event_logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    event_logger.addHandler(console_handler)

# Prevent propagation to root logger
event_logger.propagate = False
