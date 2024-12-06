import logging

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

root_logger.setLevel(logging.DEBUG)  # Use DEBUG to capture all levels

# Handlers
file_handler = logging.FileHandler(
    filename='log.txt',
    mode='w',
    encoding='utf-8'
)

# Formatters
FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s: %(message)s"
formatter = logging.Formatter(fmt=FORMAT)
file_handler.setFormatter(formatter)

root_logger.addHandler(file_handler)

__all__ = ('logger', )
