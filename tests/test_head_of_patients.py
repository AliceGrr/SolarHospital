import pytest

from exceptions import PatientsNotExistsException, StatusTooLowException
from head_of_patients import HeadOfPatients


def test_get_status():
    head_of_patients = HeadOfPatients([2, 0, 3])
    assert head_of_patients.get_status(1) == 'Слегка болен'


test_get_status_data = [
    (2, 'Тяжело болен'),
    (4, 'Болен'),
    (1, 'Слегка болен'),
    (3, 'Готов к выписке'),
]


@pytest.mark.parametrize("index,expected_state", test_get_status_data)
def test_get_status_all_statuses(index, expected_state):
    head_of_patients = HeadOfPatients([2, 0, 3, 1])

    assert head_of_patients.get_status(index) == expected_state


def test_get_status_when_patient_not_exists():
    head_of_patients = HeadOfPatients([2, 0, 3])
    with pytest.raises(PatientsNotExistsException):
        head_of_patients.get_status(5)


def test_get_status_when_no_patients():
    head_of_patients = HeadOfPatients([])
    with pytest.raises(PatientsNotExistsException):
        head_of_patients.get_status(5)


def test_status_up():
    head_of_patients = HeadOfPatients([2, 0, 3])

    head_of_patients.status_up(1)

    assert head_of_patients._patients == [3, 0, 3]


def test_status_down():
    head_of_patients = HeadOfPatients([2, 0, 3])

    head_of_patients.status_down(1)

    assert head_of_patients._patients == [1, 0, 3]


def test_status_too_low():
    head_of_patients = HeadOfPatients([2, 0, 3])

    with pytest.raises(StatusTooLowException):
        head_of_patients.status_down(2)


def test_calculate_statistics():
    patients = [3, 1, 3, 0, 0, 2, 1, 3, 2, 2, 2]
    head_of_patients = HeadOfPatients(patients)

    length, statistics = head_of_patients.get_statistics()

    assert length == len(patients)
    assert statistics == {'Тяжело болен': 2, 'Болен': 2, 'Слегка болен': 4, 'Готов к выписке': 3}


def test_calculate_statistics_when_not_all_statuses():
    patients = [1, 0, 0, 2, 1, 2, 2, 2]
    head_of_patients = HeadOfPatients(patients)

    length, statistics = head_of_patients.get_statistics()

    assert length == len(patients)
    assert statistics == {'Тяжело болен': 2, 'Болен': 2, 'Слегка болен': 4}


def test_discharge():
    head_of_patients = HeadOfPatients([2, 0, 3])

    head_of_patients.discharge(2)

    assert head_of_patients._patients == [2, 3]
