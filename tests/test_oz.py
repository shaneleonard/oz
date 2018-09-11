#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `oz_cli` package."""


from click.testing import CliRunner

from oz import cli

def test_help():
    """Test the help and usage messages."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert 'Usage' in result.output

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
