"""Basic tests for JurisAI.

This module contains basic tests for the JurisAI package.

Author: a13xh (a13x.h.cc@gmail.com)
"""


def test_import():
    """Test that the package can be imported."""
    import jurisai

    assert jurisai.__version__ == "0.1.0"