import logging

from .config import load_settings
from .logging_config import configure_logging


def main() -> None:
    settings = load_settings()

    level = logging.DEBUG if settings.debug else logging.INFO
    configure_logging(level)

    logger = logging.getLogger(__name__)
    logger.info(
        "应用启动: name=%s, env=%s",
        settings.app_name,
        settings.app_env,
    )
