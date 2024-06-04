from unittest.mock import patch, call

from coordinator import Coordinator
from dialog_with_user import DialogWithUser
from head_of_patients import HeadOfPatients
from hospital import Hospital


@patch('builtins.print')
@patch('builtins.input', side_effect=['get status', '1', 'stop'])
def test_get_status(mock_input, mock_print):
    patients = [2, 3, 1]
    head_of_patients = HeadOfPatients(patients)
    translator = DialogWithUser()
    coordinator = Coordinator(translator, head_of_patients)
    hospital = Hospital(translator, coordinator)

    hospital.start()

    assert mock_input.mock_calls == [
        call('Введите команду: '),
        call('Введите ID пациента: '),
        call('Введите команду: '),
    ]

    assert mock_print.mock_calls == [
        call('Статус пациента: "Слегка болен"'),
        call('Сеанс завершён.'),
    ]
