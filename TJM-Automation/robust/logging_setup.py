import sys
import logging
from logging.handlers import RotatingFileHandler


class LoggerFactory:
    @staticmethod
    def create_logger(name: str, log_file: str, level: str = "INFO") -> logging.Logger:
        logger = logging.getLogger(name)
        if logger.handlers:
            return logger
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(name)s %(process)d %(threadName)s - %(message)s'
        )
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        if not logging.getLogger().handlers:
            console = logging.StreamHandler(sys.stdout)
            console.setFormatter(formatter)
            logger.addHandler(console)
        return logger


