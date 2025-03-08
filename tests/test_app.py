"""Tests for the application core module.

This module contains unit tests for the main application functionality.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import signal
from unittest import mock

import pytest
import structlog

from jurisai.core.app import (
    cleanup_resources, 
    run_application, 
    setup_signal_handlers
)


@mock.patch("jurisai.core.app.signal.signal")
def test_setup_signal_handlers(mock_signal):
    """Test signal handler setup."""
    logger = mock.MagicMock()
    setup_signal_handlers(logger)
    
    # Check that signal handlers were registered
    assert mock_signal.call_count >= 2
    
    # Check SIGINT and SIGTERM were registered
    mock_signal.assert_any_call(signal.SIGINT, mock.ANY)
    mock_signal.assert_any_call(signal.SIGTERM, mock.ANY)
    
    # Get the registered handler function
    handler = mock_signal.call_args_list[0][0][1]
    
    # Test the handler
    with mock.patch("jurisai.core.app._shutdown_requested", False):
        handler(signal.SIGINT, None)
        from jurisai.core.app import _shutdown_requested
        assert _shutdown_requested is True


def test_cleanup_resources():
    """Test resource cleanup function."""
    logger = mock.MagicMock()
    cleanup_resources(logger)
    
    # Check that info messages were logged
    assert logger.info.call_count == 2
    logger.info.assert_any_call("Cleanup started", phase="pre_shutdown")
    logger.info.assert_any_call(
        "Cleanup completed", phase="post_shutdown", status="success"
    )


@mock.patch("jurisai.core.app.time.sleep")
@mock.patch("jurisai.core.app.cleanup_resources")
@mock.patch("jurisai.core.app.setup_signal_handlers")
@mock.patch("jurisai.core.app.get_logger")
def test_run_application(
    mock_get_logger, mock_setup_signal_handlers, mock_cleanup_resources, mock_sleep
):
    """Test the main application loop."""
    # Set up mocks
    mock_logger = mock.MagicMock()
    mock_get_logger.return_value = mock_logger
    
    # Set flag to request shutdown after first loop
    def side_effect(*args, **kwargs):
        from jurisai.core.app import _shutdown_requested
        import builtins
        from jurisai.core import app
        builtins.setattr(app, "_shutdown_requested", True)
    
    mock_sleep.side_effect = side_effect
    
    # Run the application
    exit_code = run_application()
    
    # Verify
    assert exit_code == 0
    mock_setup_signal_handlers.assert_called_once_with(mock_logger)
    mock_cleanup_resources.assert_called_once_with(mock_logger)
    assert mock_sleep.call_count == 1
    mock_logger.info.assert_any_call(
        "Application initialized", status="success", component="main"
    )
    mock_logger.info.assert_any_call(
        "Shutdown requested, exiting main loop", reason="signal_received"
    )
    mock_logger.info.assert_any_call(
        "Application shutdown", status="complete", app_name="JurisAI"
    )