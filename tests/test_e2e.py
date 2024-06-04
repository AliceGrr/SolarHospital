from coordinator import Coordinator
from dialog_with_user import DialogWithUser
from head_of_patients import HeadOfPatients
from hospital import Hospital
from mock_console import MockConsole


def make_application(head_of_patients, console):
    dialog_with_user = DialogWithUser(console)
    coordinator = Coordinator(dialog_with_user, head_of_patients)
    hospital = Hospital(dialog_with_user, coordinator)
    return hospital


def test_ordinary_positive_scenario():
    head_of_patients = HeadOfPatients([1, 1, 0, 2, 1])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '1')
    console.add_expected_output_message('Статус пациента: "Болен"')

    console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '1')
    console.add_expected_output_message('Новый статус пациента: "Слегка болен"')

    console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_output_message('Новый статус пациента: "Тяжело болен"')

    console.add_expected_request_and_response('Введите команду: ', 'рассчитать статистику')
    console.add_expected_output_message('В больнице на данный момент находится 5 чел., из них:\n' +
                                        '\t- в статусе "Тяжело болен": 2 чел.\n' +
                                        '\t- в статусе "Болен": 1 чел.\n' +
                                        '\t- в статусе "Слегка болен": 2 чел.\n')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(head_of_patients, console)

    app.start()

    console.verify_all_calls_have_been_made()
    # assert head_of_patients._patients == [2, 0, 0, 2, 1]


def test_unknown_command():
    head_of_patients = HeadOfPatients([])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'сделай что-нибудь...')
    console.add_expected_output_message('Неизвестная команда! Попробуйте ещё раз')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(head_of_patients, console)

    app.start()

    console.verify_all_calls_have_been_made()


def test_boundary_cases():
    head_of_patients = HeadOfPatients([0, 3, 1, 3])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '1')
    console.add_expected_output_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'да')
    console.add_expected_output_message('Пациент выписан из больницы')

    console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'нет')
    console.add_expected_output_message('Пациент остался в статусе "Готов к выписке"')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(head_of_patients, console)

    app.start()

    console.verify_all_calls_have_been_made()
    assert head_of_patients._patients == [0, 1, 3]


def test_cases_of_invalid_data_entry():
    head_of_patients = HeadOfPatients([1, 1])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', 'два')
    console.add_expected_output_message('Ошибка. ID пациента должно быть числом (целым, положительным)')

    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    console.add_expected_output_message('Ошибка. В больнице нет пациента с таким ID')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(head_of_patients, console)

    app.start()

    console.verify_all_calls_have_been_made()


def test_discharge_patient():
    head_of_patients = HeadOfPatients([1, 3, 1])
    console = MockConsole()
    console.add_expected_request_and_response('Введите команду: ', 'выписать пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_output_message('Пациент выписан из больницы')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    app = make_application(head_of_patients, console)

    app.start()

    console.verify_all_calls_have_been_made()
    assert head_of_patients._patients == [1, 1]
