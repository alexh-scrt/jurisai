"""Tests for the log_config module.

This module contains unit tests for the structured logging configuration.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import logging
from unittest import mock

import pytest
import structlog

from jurisai.utils.log_config import configure_logging, get_logger


@mock.patch("jurisai.utils.log_config.structlog.configure")
@mock.patch("jurisai.utils.log_config.logging.basicConfig")
def test_configure_logging(mock_basic_config, mock_structlog_configure):
    """Test logging configuration with default parameters."""
    configure_logging()
    
    mock_basic_config.assert_called_once()
    mock_structlog_configure.assert_called_once()
    
    # Test that level is correctly passed
    configure_logging(level=logging.DEBUG)
    assert mock_basic_config.call_args[1]["level"] == logging.DEBUG


@mock.patch("jurisai.utils.log_config.structlog.get_logger")
def test_get_logger(mock_get_logger):
    """Test getting a structured logger."""
    logger_name = "test_logger"
    get_logger(logger_name)
    mock_get_logger.assert_called_once_with(logger_name)


def test_get_logger_returns_bound_logger():
    """Test that get_logger returns a BoundLogger instance."""
    logger = get_logger("test")
    assert isinstance(logger, structlog.stdlib.BoundLogger)