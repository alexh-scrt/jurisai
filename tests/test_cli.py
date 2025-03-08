"""Tests for the CLI module.

This module contains unit tests for the command-line interface.

Author: a13xh (a13x.h.cc@gmail.com)
"""

import logging
from unittest import mock

import pytest

from jurisai.cli.commands import main, parse_args


def test_parse_args():
    """Test the argument parser."""
    args = parse_args(["--verbose"])
    assert args.verbose is True
    
    args = parse_args([])
    assert args.verbose is False
    
    # Test analyze command
    args = parse_args(["analyze", "document.pdf"])
    assert args.command == "analyze"
    assert args.file == "document.pdf"
    
    # Test search command
    args = parse_args(["search", "legal precedent"])
    assert args.command == "search"
    assert args.query == "legal precedent"


@mock.patch("jurisai.cli.commands.configure_logging")
def test_main_with_analyze_command(mock_configure_logging):
    """Test the main function with analyze command."""
    with mock.patch("jurisai.cli.commands.parse_args") as mock_parse_args:
        # Setup mock
        mock_args = mock.MagicMock()
        mock_args.verbose = True
        mock_args.command = "analyze"
        mock_args.file = "test.pdf"
        mock_parse_args.return_value = mock_args
        
        # Call main
        result = main([])
        
        # Verify
        assert result == 0
        mock_configure_logging.assert_called_once_with(level="DEBUG")


@mock.patch("jurisai.cli.commands.configure_logging")
def test_main_with_search_command(mock_configure_logging):
    """Test the main function with search command."""
    with mock.patch("jurisai.cli.commands.parse_args") as mock_parse_args:
        # Setup mock
        mock_args = mock.MagicMock()
        mock_args.verbose = False
        mock_args.command = "search"
        mock_args.query = "test query"
        mock_parse_args.return_value = mock_args
        
        # Call main
        result = main([])
        
        # Verify
        assert result == 0
        mock_configure_logging.assert_called_once_with(level="INFO")


@mock.patch("jurisai.cli.commands.run_application")
@mock.patch("jurisai.cli.commands.configure_logging")
def test_main_with_no_command(mock_configure_logging, mock_run_application):
    """Test the main function with no command (interactive mode)."""
    with mock.patch("jurisai.cli.commands.parse_args") as mock_parse_args:
        # Setup mock
        mock_args = mock.MagicMock()
        mock_args.verbose = False
        mock_args.command = None  # No command
        mock_parse_args.return_value = mock_args
        mock_run_application.return_value = 0
        
        # Call main
        result = main([])
        
        # Verify
        assert result == 0
        mock_run_application.assert_called_once()
        mock_configure_logging.assert_called_once_with(level="INFO")