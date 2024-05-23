import unittest
from unittest.mock import MagicMock

from coordinator import Coordinator


class TestCoordinator(unittest.TestCase):
    def test_get_status(self):
        coordinator = Coordinator(MagicMock())
        coordinator._head_of_patients.get_status = MagicMock(return_value=1)
        coordinator._translator.ask_id = MagicMock(return_value=1)
        coordinator._translator.answer_status = MagicMock()

        coordinator.get_status()

        coordinator._translator.answer_status.assert_called_with(1)

    def test_get_status_with_unknown_id(self):
        coordinator = Coordinator(MagicMock())
        coordinator._head_of_patients.get_status = MagicMock(return_value=1)
        coordinator._translator.ask_id = MagicMock(return_value=1)
        coordinator._translator.answer_status = MagicMock()

        coordinator.get_status()

        coordinator._translator.answer_status.assert_called_with(1)

    def test_status_up_and_discharge(self):
        coordinator = Coordinator(MagicMock())
        coordinator._head_of_patients.get_status = MagicMock(return_value=1)
        coordinator._translator.ask_id = MagicMock(return_value=1)
        coordinator._translator.answer_status = MagicMock()

        coordinator.get_status()

        coordinator._translator.answer_status.assert_called_with(1)

    def test_make_status_too_low(self):
        coordinator = Coordinator(MagicMock())
        coordinator._head_of_patients.get_status = MagicMock(return_value=1)
        coordinator._translator.ask_id = MagicMock(return_value=1)
        coordinator._translator.answer_status = MagicMock()

        coordinator.get_status()

        coordinator._translator.answer_status.assert_called_with(1)
