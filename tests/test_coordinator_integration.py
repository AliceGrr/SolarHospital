from unittest.mock import MagicMock

from coordinator import Coordinator
from exceptions import PatientsNotExistsException, StatusTooLowException
from head_of_patients import HeadOfPatients


def test_get_status():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.get_status()

    coordinator._translator.answer_patient_status.assert_called_with('Слегка болен')


def test_get_status_when_patient_not_exists():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=5)

    coordinator.get_status()

    coordinator._translator.answer.assert_called_with(PatientsNotExistsException.message)


def test_status_up():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=1)

    coordinator.status_up()

    coordinator._translator.answer_patient_status_changed.assert_called_with('Готов к выписке')
    assert coordinator._head_of_patients._patients == [3, 3, 1]


def test_status_up_when_max_status_and_agree_to_discharge_patient():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)
    coordinator._translator.ask_agreement_to_discharge_patient = MagicMock(return_value=True)

    coordinator.status_up()

    # Просто asser called, потому что туда не передаются параметры
    coordinator._translator.answer_patient_discharged.assert_called()
    assert coordinator._head_of_patients._patients == [2, 1]


def test_status_up_when_max_status_and_disagree_to_discharge_patient():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)
    coordinator._translator.ask_agreement_to_discharge_patient = MagicMock(return_value=False)

    coordinator.status_up()

    coordinator._translator.answer_patient_status_not_changed.assert_called_with('Готов к выписке')
    assert coordinator._head_of_patients._patients == [2, 3, 1]


def test_status_up_when_patient_not_exists():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=5)

    coordinator.status_up()

    coordinator._translator.answer.assert_called_with(PatientsNotExistsException.message)


def test_status_down():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)

    coordinator.status_down()

    coordinator._translator.answer_patient_status_changed.assert_called_with('Слегка болен')
    assert coordinator._head_of_patients._patients == [2, 2, 1]


def test_status_down_when_min_patient_status():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 0, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)

    coordinator.status_down()

    coordinator._translator.answer.assert_called_with(StatusTooLowException.message)
    assert coordinator._head_of_patients._patients == [2, 0, 1]


def test_status_down_when_patient_not_exists():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=5)

    coordinator.status_down()

    coordinator._translator.answer.assert_called_with(PatientsNotExistsException.message)


def test_discharge():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=2)

    coordinator.discharge()

    coordinator._translator.answer_patient_discharged.assert_called()
    assert coordinator._head_of_patients._patients == [2, 1]


def test_discharge_when_patient_not_exists():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([2, 3, 1]))
    coordinator._translator.ask_id = MagicMock(return_value=5)

    coordinator.discharge()

    coordinator._translator.answer.assert_called_with(PatientsNotExistsException.message)
    assert coordinator._head_of_patients._patients == [2, 3, 1]


def test_calculate_statistics():
    patients = [3, 1, 3, 0, 0, 2, 1, 3, 2, 2, 2]
    coordinator = Coordinator(MagicMock(), HeadOfPatients(patients))

    coordinator.calculate_statistics()

    statistics_text = '\n'.join([
        f'В больнице на данный момент находится {len(patients)} чел., из них:',
        '\t- в статусе "Тяжело болен": 2 чел.',
        '\t- в статусе "Болен": 2 чел.',
        '\t- в статусе "Слегка болен": 4 чел.',
        '\t- в статусе "Готов к выписке": 3 чел.\n'
    ])

    coordinator._translator.answer.assert_called_with(statistics_text)


def test_calculate_statistics_when_empty_patients_list():
    coordinator = Coordinator(MagicMock(), HeadOfPatients([]))

    coordinator.calculate_statistics()

    coordinator._translator.answer.assert_called_with('В больнице на данный момент нет пациентов. Все вылечились :)')
