import logging


logger = logging.getLogger(__name__)

logger_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logger_formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)
