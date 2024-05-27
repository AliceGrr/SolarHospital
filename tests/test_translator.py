from unittest.mock import patch

import pytest

from exceptions import InvalidIDException
from translator import Translator

valid_commands = ['get status', 'GET status', 'узнать статус пациента']


@patch('builtins.input', side_effect=['get status'])
def test_ask_command(_):
    translator = Translator()
    assert translator.ask_command() == 'get_status'


@pytest.mark.parametrize('command', valid_commands)
def test_translate_command(command):
    translator = Translator()
    assert translator._translate_command_input(command) == 'get_status'


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
        translator._validate_and_translate_id_input('id')


def test_get_double_id():
    translator = Translator()

    with pytest.raises(InvalidIDException):
        translator._validate_and_translate_id_input('1.5')


def test_get_negative_id():
    translator = Translator()

    with pytest.raises(InvalidIDException):
        translator._validate_and_translate_id_input('-1')


if __name__ == '__main__':
    test_ask_command()
    test_get_str_id()
    test_get_zero_id()
    test_get_negative_id()
    test_get_double_id()
    test_get_unknown_command()
    test_get_valid_id()
    test_translate_command()