import logging

def setup_logging(level=logging.DEBUG):
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")
