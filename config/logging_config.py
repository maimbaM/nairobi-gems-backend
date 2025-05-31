import logging


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Avoid duplicate handlers if already configured
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
