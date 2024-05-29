from unittest.mock import MagicMock

from coordinator import Coordinator
from head_of_patients import HeadOfPatients


def test_get_status():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.get_status()

    coordinator._translator.answer_status.assert_called_with('Слегка болен')


def test_get_status_when_patient_not_exists():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=5)

    coordinator.get_status()

    coordinator._translator.answer_exception.assert_called()


def test_status_up():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.status_up()

    coordinator._translator.answer_status_changed.assert_called()
    assert coordinator._head_of_patients._patients == [3, 3, 1]


def test_status_up_and_discharge():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)
    coordinator._translator.ask_agreement = MagicMock(return_value=True)

    coordinator.status_up()

    coordinator._translator.answer_discharged.assert_called()
    assert coordinator._head_of_patients._patients == [2, 1]


def test_status_up_and_no_discharge():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)
    coordinator._translator.ask_agreement = MagicMock(return_value=False)

    coordinator.status_up()

    coordinator._translator.answer_status_not_changed.assert_called()
    assert coordinator._head_of_patients._patients == [2, 3, 1]
