from unittest.mock import MagicMock
from coordinator import Coordinator
from exceptions import UnknownIDException
from head_of_patients import HeadOfPatients


def test_get_status():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([1]))
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.get_status()
    coordinator._translator.answer_status.assert_called_with('Болен')


def test_get_status_with_unknown_id():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([]))
    ex = UnknownIDException()
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.get_status()
    coordinator._translator.answer_exception.assert_called()


def test_status_up_and_discharge():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([3]))
    coordinator._translator.ask_id = MagicMock(return_value=1)
    coordinator._translator.ask_agreement = MagicMock(return_value='да')

    coordinator.status_up()
    coordinator._translator.answer_discharged.assert_called()


if __name__ == '__main__':
    test_get_status()
    test_get_status_with_unknown_id()
    test_status_up_and_discharge()
