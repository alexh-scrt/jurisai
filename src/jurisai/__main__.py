"""Entry point for running the package as a script.

This module allows the package to be executed directly using
`python -m src.jurisai`.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import sys
from src.jurisai.cli.commands import main

if __name__ == "__main__":
    sys.exit(main())