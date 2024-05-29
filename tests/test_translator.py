from unittest.mock import patch

import pytest

from exceptions import InvalidIDException
from translator import Translator

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


@patch('builtins.input', side_effect=['get status'])
def test_ask_command(_):
    translator = Translator()

    assert translator.ask_command() == 'get_status'


@pytest.mark.parametrize('user_input,command', valid_commands)
def test_translate_user_input_into_command(user_input, command):
    translator = Translator()

    assert translator._translate_command_input(user_input) == command


def test_translate_command_when_letters_of_different_case():
    translator = Translator()

    assert translator._translate_command_input('GET status') == 'get_status'


def test_get_unknown_command():
    translator = Translator()

    assert translator._translate_command_input('command') is None


def test_get_valid_id():
    translator = Translator()
    assert translator._validate_and_translate_id_input('1') == 1


def test_get_zero_id():
    translator = Translator()

    with pytest.raises(InvalidIDException):
        translator._validate_and_translate_id_input('0')


def test_get_str_id():
    translator = Translator()

    with pytest.raises(InvalidIDException):
        translator._validate_and_translate_id_input('два')


def test_get_double_id():
    translator = Translator()

    with pytest.raises(InvalidIDException):
        translator._validate_and_translate_id_input('1.5')


def test_get_negative_id():
    translator = Translator()

    with pytest.raises(InvalidIDException):
        translator._validate_and_translate_id_input('-1')
