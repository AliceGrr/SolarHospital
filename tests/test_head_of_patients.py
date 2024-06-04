import pytest

from exceptions import PatientsNotExistsException, StatusTooLowException
from head_of_patients import HeadOfPatients


def test_get_status():
    head_of_patients = HeadOfPatients([2, 0, 3])
    assert head_of_patients.get_status(1) == 'Слегка болен'


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


def test_status_up_when_patient_not_exists():
    head_of_patients = HeadOfPatients([2, 0, 3])

    with pytest.raises(PatientsNotExistsException):
        head_of_patients.status_up(5)


def test_status_down():
    head_of_patients = HeadOfPatients([2, 0, 3])

    head_of_patients.status_down(1)

    assert head_of_patients._patients == [1, 0, 3]


def test_status_down_when_patient_not_exists():
    head_of_patients = HeadOfPatients([2, 0, 3])

    with pytest.raises(PatientsNotExistsException):
        head_of_patients.status_down(5)


def test_status_down_when_status_minimum():
    head_of_patients = HeadOfPatients([2, 0, 3])

    with pytest.raises(StatusTooLowException):
        head_of_patients.status_down(2)


def test_calculate_statistics():
    patients = [3, 1, 3, 0, 0, 2, 1, 3, 2, 2, 2]
    head_of_patients = HeadOfPatients(patients)

    length, statistics = head_of_patients.get_statistics()

    assert length == len(patients)
    assert statistics == {'Тяжело болен': 2, 'Болен': 2, 'Слегка болен': 4, 'Готов к выписке': 3}


def test_calculate_statistics_when_patient_list_has_not_all_possible_statuses():
    patients = [0, 2, 0, 2, 2]
    head_of_patients = HeadOfPatients(patients)

    _, statistics = head_of_patients.get_statistics()

    assert statistics == {'Тяжело болен': 2, 'Слегка болен': 3}


def test_calculate_statistics_when_empty_patients_list():
    head_of_patients = HeadOfPatients([])

    _, statistics = head_of_patients.get_statistics()

    assert statistics == {}


def test_discharge():
    head_of_patients = HeadOfPatients([2, 0, 3])

    head_of_patients.discharge(2)

    assert head_of_patients._patients == [2, 3]


def test_discharge_when_patient_not_exists():
    head_of_patients = HeadOfPatients([2, 0, 3])

    with pytest.raises(PatientsNotExistsException):
        head_of_patients.discharge(5)

