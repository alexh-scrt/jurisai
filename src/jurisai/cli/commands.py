"""Command line interface for JurisAI.

This module contains the command-line argument parsing and execution.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import argparse
import sys
from typing import List, Optional

from src.jurisai import __version__
from src.jurisai.core.app import run_application
from src.jurisai.utils.log_config import configure_logging, get_logger


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: Command line arguments. Defaults to sys.argv.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="JurisAI - AI-powered legal assistant"
    )
    parser.add_argument(
        "--version", action="version", version=f"JurisAI {__version__}"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Web UI command
    web_parser = subparsers.add_parser("web", help="Launch the web interface")
    web_parser.add_argument(
        "--port", type=int, default=8501, help="Port to run the web server on"
    )
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze legal documents")
    analyze_parser.add_argument("file", help="File to analyze")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search legal database")
    search_parser.add_argument("query", help="Search query")
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Run the main application.

    Args:
        args: Command line arguments. Defaults to sys.argv.

    Returns:
        Exit code.
    """
    parsed_args = parse_args(args)
    
    # Set up logging
    log_level = "DEBUG" if parsed_args.verbose else "INFO"
    configure_logging(level=log_level)
    
    logger = get_logger(__name__)
    logger.info("Application starting", version=__version__, app_name="JurisAI")
    
    try:
        # Run the appropriate command
        if parsed_args.command == "web":
            logger.info("Launching web interface", port=parsed_args.port)
            # Launch Streamlit app
            import subprocess
            import os
            
            # Get the path to the Streamlit app
            streamlit_app_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "api",
                "streamlit_app.py"
            )
            
            # Run Streamlit as a subprocess
            cmd = [
                "streamlit", "run", 
                streamlit_app_path,
                "--server.port", str(parsed_args.port)
            ]
            
            logger.info("Running Streamlit", command=" ".join(cmd))
            
            # Execute the command
            process = subprocess.run(cmd)
            return process.returncode
            
        elif parsed_args.command == "analyze":
            logger.info("Analyzing document", file=parsed_args.file)
            # Call the appropriate function
            # analyze_document(parsed_args.file)
        elif parsed_args.command == "search":
            logger.info("Searching database", query=parsed_args.query)
            # Call the appropriate function
            # search_database(parsed_args.query)
        else:
            # Default behavior: run the interactive application
            return run_application()
            
        return 0
    except Exception as e:
        logger.exception("Fatal application error", 
                       error_type=type(e).__name__, 
                       error_msg=str(e),
                       component="main")
        return 1