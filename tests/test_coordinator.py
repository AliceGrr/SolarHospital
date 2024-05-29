from unittest.mock import MagicMock

from coordinator import Coordinator
from exceptions import PatientsNotExistsException


def test_get_status():
    coordinator = Coordinator(MagicMock(), MagicMock())
    coordinator._head_of_patients.get_status = MagicMock(return_value='Болен')
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.get_status()

    coordinator._translator.answer_status.assert_called_with('Болен')


def test_get_status_when_patient_not_exists():
    coordinator = Coordinator(MagicMock(), MagicMock())
    ex = PatientsNotExistsException()
    coordinator._head_of_patients.get_status = MagicMock(side_effect=ex)
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.get_status()

    coordinator._translator.answer_exception.assert_called_with(ex)