from unittest.mock import patch, call

from console import Console
from coordinator import Coordinator
from dialog_with_user import DialogWithUser
from head_of_patients import HeadOfPatients
from hospital import Hospital


@patch('builtins.print')
@patch('builtins.input', side_effect=['get status', '1', 'stop'])
def test_get_status(mock_input, mock_print):
    patients = [2, 3, 1]
    head_of_patients = HeadOfPatients(patients)
    console = Console()
    dialog_with_user = DialogWithUser(console)
    coordinator = Coordinator(dialog_with_user, head_of_patients)
    hospital = Hospital(dialog_with_user, coordinator)

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
