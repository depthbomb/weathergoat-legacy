from sys import stdout
from loguru import logger
from src.constants import DEBUG

logger.remove()
logger.level("DEBUG", color="<light-black>")
logger.level("INFO", color="<light-blue>")
logger.level("ERROR", color="<light-red><b>")
logger.add(
    stdout,
    level="TRACE" if DEBUG else "INFO",
    format="{time:HH:mm:ss} │ <level>{level: <8}</level> │ <fg #fff>{message}</fg #fff>",
    colorize=True,
    backtrace=True,
    diagnose=DEBUG,
    enqueue=True
)
