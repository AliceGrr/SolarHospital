import unittest
from unittest.mock import patch

from exceptions import InvalidIDException
from translator import Translator


class TestTranslator(unittest.TestCase):
    @patch('builtins.input', side_effect=['get status', 'узнать статус пациента', 'Get STatUs'])
    def test_get_command(self, _):
        translator = Translator()
        assert translator.ask_command() == 'get_status'
        assert translator.ask_command() == 'get_status'
        assert translator.ask_command() == 'get_status'

    @patch('builtins.input', side_effect=['command'])
    def test_get_unknown_command(self, _):
        translator = Translator()
        assert translator.ask_command() is None

    @patch('builtins.input', side_effect=['1'])
    def test_get_valid_id(self, _):
        translator = Translator()
        assert translator.ask_id() == 0

    @patch('builtins.input', side_effect=['-1', '1,5', '4.1', 'number'])
    def test_get_invalid_id(self, _):
        translator = Translator()

        with self.assertRaises(InvalidIDException):
            translator.ask_id()
        with self.assertRaises(InvalidIDException):
            translator.ask_id()
        with self.assertRaises(InvalidIDException):
            translator.ask_id()
        with self.assertRaises(InvalidIDException):
            translator.ask_id()
