import logging
import structlog
from pathlib import Path

from logging.handlers import TimedRotatingFileHandler
from structlog.threadlocal import merge_threadlocal


def setup_logging(log_dir, log_level=logging.INFO):
    # avoid double logging by uvicorn
    logging.getLogger("uvicorn").removeHandler(logging.getLogger("uvicorn").handlers[0])

    # convert possible string definition to int/fn
    log_level = getattr(logging, log_level) if isinstance(log_level, str) else log_level

    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

    shared_processors = [
        merge_threadlocal,
        timestamper,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure_once(
        processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(), foreign_pre_chain=shared_processors
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # create log directory
    p = Path(log_dir)
    p.mkdir(exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        p / "log.log", when="D", interval=1, backupCount=7
    )
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(log_level)
