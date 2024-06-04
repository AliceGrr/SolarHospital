from unittest.mock import patch

import pytest

from console import Console
from exceptions import InvalidIDException
from dialog_with_user import DialogWithUser


@patch('builtins.input', side_effect=['get status'])
def test_ask_command(_):
    console = Console()
    dialog_with_user = DialogWithUser(console)

    assert dialog_with_user.ask_command() == 'get_status'


valid_commands = [
    ('get status', 'get_status'),
    ('узнать статус пациента', 'get_status'),

    ('status up', 'status_up'),
    ('повысить статус пациента', 'status_up'),

    ('status down', 'status_down'),
    ('понизить статус пациента', 'status_down'),

    ('discharge', 'discharge'),
    ('выписать пациента', 'discharge'),

    ('calculate statistics', 'calculate_statistics'),
    ('рассчитать статистику', 'calculate_statistics'),

    ('stop', 'stop'),
    ('стоп', 'stop'),
]


@pytest.mark.parametrize('user_input,command', valid_commands)
def test_convert_user_input_into_command(user_input, command):
    console = Console()
    dialog_with_user = DialogWithUser(console)

    assert dialog_with_user._convert_user_input_to_command(user_input) == command


def test_convert_command_when_letters_of_different_case():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    assert dialog_with_user._convert_user_input_to_command('GET status') == 'get_status'


def test_convert_command_when_got_unknown_command():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    assert dialog_with_user._convert_user_input_to_command('выпиши всех') == 'unknown'


def test_convert_command_when_got_valid_id():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    assert dialog_with_user._convert_str_user_input_to_int_id('1') == 1


def test_convert_command_when_got_zero_id():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    with pytest.raises(InvalidIDException):
        dialog_with_user._convert_str_user_input_to_int_id('0')


def test_convert_command_when_got_str_id():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    with pytest.raises(InvalidIDException):
        dialog_with_user._convert_str_user_input_to_int_id('два')


def test_convert_command_when_got_double_id():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    with pytest.raises(InvalidIDException):
        dialog_with_user._convert_str_user_input_to_int_id('1.5')


def test_convert_command_when_got_negative_id():
    console = Console()
    dialog_with_user = DialogWithUser(console)

    with pytest.raises(InvalidIDException):
        dialog_with_user._convert_str_user_input_to_int_id('-1')
