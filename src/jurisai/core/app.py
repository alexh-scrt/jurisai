"""Core application module for JurisAI.

This module contains the main application logic and signal handling.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import signal
import time
from typing import Any, Dict, Optional

import structlog

from src.jurisai.utils.log_config import get_logger


# Global flag for graceful shutdown
_shutdown_requested = False


def setup_signal_handlers(logger: structlog.stdlib.BoundLogger) -> None:
    """Set up signal handlers for graceful shutdown.

    Args:
        logger: Structured logger instance for messages.
    """
    global _shutdown_requested

    def signal_handler(sig: int, frame: Any) -> None:
        """Handle signals to gracefully shutdown.

        Args:
            sig: Signal number.
            frame: Current stack frame.
        """
        global _shutdown_requested
        signame = signal.Signals(sig).name
        logger.info("Received signal, initiating shutdown", signal=signame, signal_number=sig)
        _shutdown_requested = True

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)   # Keyboard interrupt (Ctrl+C)
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    # On Unix-like systems, also handle SIGHUP
    if hasattr(signal, "SIGHUP"):
        signal.signal(signal.SIGHUP, signal_handler)  # Terminal closed


def cleanup_resources(logger: structlog.stdlib.BoundLogger) -> None:
    """Perform cleanup operations before exit.

    Args:
        logger: Structured logger instance for messages.
    """
    logger.info("Cleanup started", phase="pre_shutdown")
    # Close any open files, database connections, etc.
    # Release any resources, save state, etc.
    logger.info("Cleanup completed", phase="post_shutdown", status="success")


def run_application() -> int:
    """Run the main application loop.

    Returns:
        Exit code.
    """
    global _shutdown_requested
    
    logger = get_logger(__name__)
    
    # Set up signal handlers
    setup_signal_handlers(logger)
    
    try:
        logger.info("Application initialized", status="success", component="main")

        # Main application loop
        while not _shutdown_requested:
            # Your application logic here
            # For example purposes, we'll just sleep
            time.sleep(0.1)
            
            # Check for shutdown condition
            if _shutdown_requested:
                logger.info("Shutdown requested, exiting main loop", reason="signal_received")
                break
                
        return 0
    except Exception as e:
        logger.exception("Application error", 
                       error_type=type(e).__name__,
                       error_msg=str(e),
                       component="main_loop")
        return 1
    finally:
        # Always perform cleanup
        cleanup_resources(logger)
        logger.info("Application shutdown", status="complete", app_name="JurisAI")