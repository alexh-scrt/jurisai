#!/usr/bin/env python3
"""
Main entry script for JurisAI.

This script provides a convenient way to start the application
directly from the project root without installing the package.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import sys
import os

# Add the parent directory to sys.path to allow importing from src
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.jurisai.cli.commands import main


if __name__ == "__main__":
    # Call the main CLI entry point
    sys.exit(main(sys.argv[1:]))