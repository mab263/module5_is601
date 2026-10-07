"""
Unit tests for app/calculator_repl.py.

Tests the REPL (Read-Eval-Print Loop) interface, covering all supported
commands, arithmetic operations, and error handling paths.
"""

import pytest

from unittest.mock import patch
from app.calculator_repl import calculator_repl


@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")


@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")


@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")


@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
def test_calculator_repl_history_empty(mock_print, mock_input):
    with patch('app.calculator.Calculator.show_history', return_value=[]):
        calculator_repl()
        mock_print.assert_any_call("No calculations in history")


@patch('builtins.input', side_effect=['add', '2', '3', 'history', 'exit'])
@patch('builtins.print')
def test_calculator_repl_history_with_entries(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nCalculation History:")


@patch('builtins.input', side_effect=['add', '2', '3', 'clear', 'exit'])
@patch('builtins.print')
def test_calculator_repl_clear(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History cleared")


@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_undo_nothing(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to undo")


@patch('builtins.input', side_effect=['add', '2', '3', 'undo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_undo_success(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation undone")


@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_redo_nothing(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to redo")


@patch('builtins.input', side_effect=['add', '2', '3', 'undo', 'redo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_redo_success(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation redone")


@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calculator_repl_save_success(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History saved successfully")


@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calculator_repl_save_failure(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history', side_effect=Exception("disk full")):
        calculator_repl()
        found = any("Error saving history" in str(call) for call in mock_print.call_args_list)
        assert found


@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calculator_repl_load_success(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History loaded successfully")


@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calculator_repl_load_failure(mock_print, mock_input):
    with patch('app.calculator.Calculator.load_history', side_effect=Exception("file corrupt")):
        calculator_repl()
        found = any("Error loading history" in str(call) for call in mock_print.call_args_list)
        assert found


@patch('builtins.input', side_effect=['subtract', '10', '4', 'exit'])
@patch('builtins.print')
def test_calculator_repl_subtract(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 6")


@patch('builtins.input', side_effect=['multiply', '3', '4', 'exit'])
@patch('builtins.print')
def test_calculator_repl_multiply(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 12")


@patch('builtins.input', side_effect=['divide', '10', '2', 'exit'])
@patch('builtins.print')
def test_calculator_repl_divide(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")


@patch('builtins.input', side_effect=['power', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_power(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 8")


@patch('builtins.input', side_effect=['root', '9', '2', 'exit'])
@patch('builtins.print')
def test_calculator_repl_root(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 3")


@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
def test_calculator_repl_cancel_first_number(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")


@patch('builtins.input', side_effect=['add', '2', 'cancel', 'exit'])
@patch('builtins.print')
def test_calculator_repl_cancel_second_number(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")


@patch('builtins.input', side_effect=['divide', '10', '0', 'exit'])
@patch('builtins.print')
def test_calculator_repl_validation_or_operation_error(mock_print, mock_input):
    calculator_repl()
    found = any("Error:" in str(call) for call in mock_print.call_args_list)
    assert found


@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_unexpected_error_during_operation(mock_print, mock_input):
    with patch('app.calculator.Calculator.perform_operation', side_effect=Exception("boom")):
        calculator_repl()
        found = any("Unexpected error" in str(call) for call in mock_print.call_args_list)
        assert found


@patch('builtins.input', side_effect=['bogus', 'exit'])
@patch('builtins.print')
def test_calculator_repl_unknown_command(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Unknown command: 'bogus'. Type 'help' for available commands.")


@patch('builtins.input', side_effect=KeyboardInterrupt())
@patch('builtins.print')
def test_calculator_repl_keyboard_interrupt(mock_print, mock_input):
    with patch('app.calculator_repl.input', side_effect=[KeyboardInterrupt(), 'exit']):
        calculator_repl()
        mock_print.assert_any_call("\nOperation cancelled")


@patch('builtins.input', side_effect=EOFError())
@patch('builtins.print')
def test_calculator_repl_eof_error(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nInput terminated. Exiting...")


@patch('builtins.print')
def test_calculator_repl_fatal_initialization_error(mock_print):
    with patch('app.calculator_repl.Calculator', side_effect=Exception("init failed")):
        with pytest.raises(Exception, match="init failed"):
            calculator_repl()
        found = any("Fatal error" in str(call) for call in mock_print.call_args_list)
        assert found


@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
def test_calculator_repl_outer_unexpected_exception(mock_print, mock_input):
    with patch('app.calculator.Calculator.show_history', side_effect=Exception("boom")):
        calculator_repl()
        found = any("Error: boom" in str(call) for call in mock_print.call_args_list)
        assert found

