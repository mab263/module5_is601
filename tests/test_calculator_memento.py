"""
Unit tests for app/calculator_memento.py.

Tests the CalculatorMemento class, which implements the Memento pattern
for saving and restoring calculator state (undo/redo functionality).
"""

import datetime
from decimal import Decimal

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


def test_memento_stores_history_and_timestamp():
    """
    Test that a CalculatorMemento correctly stores a history list and timestamp.
    """
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    memento = CalculatorMemento(history=[calc])

    assert memento.history == [calc]
    assert isinstance(memento.timestamp, datetime.datetime)


def test_memento_to_dict():
    """
    Test that to_dict() correctly serializes the memento's history and timestamp.
    """
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    timestamp = datetime.datetime(2024, 1, 1, 12, 0, 0)
    memento = CalculatorMemento(history=[calc], timestamp=timestamp)

    result = memento.to_dict()

    assert result['timestamp'] == timestamp.isoformat()
    assert len(result['history']) == 1
    assert result['history'][0] == calc.to_dict()


def test_memento_from_dict():
    """
    Test that from_dict() correctly reconstructs a CalculatorMemento instance
    from a dictionary representation.
    """
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    timestamp = datetime.datetime(2024, 1, 1, 12, 0, 0)
    data = {
        'history': [calc.to_dict()],
        'timestamp': timestamp.isoformat()
    }

    memento = CalculatorMemento.from_dict(data)

    assert memento.timestamp == timestamp
    assert len(memento.history) == 1
    assert memento.history[0].operation == calc.operation
    assert memento.history[0].operand1 == calc.operand1
    assert memento.history[0].operand2 == calc.operand2


def test_memento_round_trip():
    """
    Test that converting a memento to a dict and back preserves its state.
    """
    calc = Calculation(operation="Multiplication", operand1=Decimal("4"), operand2=Decimal("5"))
    original = CalculatorMemento(history=[calc])

    data = original.to_dict()
    restored = CalculatorMemento.from_dict(data)

    assert restored.history[0].operation == original.history[0].operation
    assert restored.history[0].operand1 == original.history[0].operand1
    assert restored.history[0].operand2 == original.history[0].operand2
