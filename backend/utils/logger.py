import logging


def setup_logger(
    name: str, level: int = logging.DEBUG, file: str = None
) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] %(name)s %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if file:
        fh = logging.FileHandler(file)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


bot_logger = setup_logger("[BOT]")
vpn_logger = setup_logger("[VPN]")