"""Structured logging configuration for JurisAI.

This module configures structured logging for the application using structlog.
It sets up console output with rich formatting for development and JSON output
for production environments.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import json
import logging
import sys
import time
from typing import Any, Dict, List, Optional, Union, cast

import rich.console
import structlog
from rich.logging import RichHandler


def configure_logging(level: Union[int, str] = logging.INFO) -> None:
    """Configure structured logging for the application.

    Sets up structlog with processors for context, timestamps, and formatting.
    Configures console output with rich formatting.

    Args:
        level: The logging level to use. Can be a string name or integer level.
    """
    # Convert string level to int if needed
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())

    # Configure standard logging
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )

    # Set timestamp format
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure structlog's formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        # Format for non-JSON output
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(colors=True, exception_formatter=rich_exception_formatter),
        ],
        # Keep foreign_pre_chain for handling non-structlog logs
        foreign_pre_chain=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.format_exc_info,
        ],
    )

    # Add a handler with our formatter to the root logger
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]

    # Suppress overly verbose logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def rich_exception_formatter(sio: Any, exc_info: Any) -> None:
    """Format exceptions with rich traceback.

    Args:
        sio: StringIO-like object to write to.
        exc_info: Exception info tuple.
    """
    console = rich.console.Console(file=sio, width=140)
    console.print_exception(show_locals=True)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger with the given name.

    Args:
        name: The name for the logger, typically __name__.

    Returns:
        A structured logger instance bound with the given name.
    """
    return structlog.get_logger(name)