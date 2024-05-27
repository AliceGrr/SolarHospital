import pytest

from exceptions import UnknownIDException, StatusTooLowException
from head_of_patients import HeadOfPatients

test_get_status_data = [
    ([0], 1, 'Тяжело болен'),
    ([1], 1, 'Болен'),
    ([2], 1, 'Слегка болен'),
    ([3], 1, 'Готов к выписке'),
]


@pytest.mark.parametrize("patients,index,expected", test_get_status_data)
def test_get_status(patients, index, expected):
    head_of_patients = HeadOfPatients(patients)
    assert head_of_patients.get_status(index) == expected


def test_get_unknown_id():
    head_of_patients = HeadOfPatients([])
    with pytest.raises(UnknownIDException):
        head_of_patients.get_status(1)


def test_status_up():
    head_of_patients = HeadOfPatients([1])
    head_of_patients.status_up(1)
    assert head_of_patients.get_status(1) == 'Слегка болен'


def test_status_down():
    head_of_patients = HeadOfPatients([1])
    head_of_patients.status_down(1)
    assert head_of_patients.get_status(1) == 'Тяжело болен'


def test_status_too_low():
    head_of_patients = HeadOfPatients([0])
    with pytest.raises(StatusTooLowException):
        head_of_patients.status_down(1)


def test_calculate_statistics():
    patients = [0, 1, 1, 2, 2, 2, 3, 3, 3, 3]
    head_of_patients = HeadOfPatients(patients)
    length, statistics = head_of_patients.get_statistics()
    assert length == len(patients)
    assert statistics == {'Тяжело болен': 1, 'Болен': 2, 'Слегка болен': 3, 'Готов к выписке': 4}


def test_discharge():
    head_of_patients = HeadOfPatients([1])
    head_of_patients.discharge(1)
    assert len(head_of_patients._patients) == 0


if __name__ == '__main__':
    test_discharge()
    test_calculate_statistics()
    test_status_too_low()
    test_status_up()
    test_status_down()
    test_get_status()
    test_get_unknown_id()
