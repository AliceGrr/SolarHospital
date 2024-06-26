from exceptions import InvalidIDException


class DialogWithUser:

    def __init__(self, console):
        self._console = console
        self._commands = {
            'get_status': ('get status', 'узнать статус пациента'),
            'status_up': ('status up', 'повысить статус пациента'),
            'status_down': ('status down', 'понизить статус пациента'),
            'discharge': ('discharge', 'выписать пациента'),
            'calculate_statistics': ('calculate statistics', 'рассчитать статистику'),
            'stop': ('stop', 'стоп')
        }

    def _convert_str_user_input_to_int_id(self, user_input):
        if '.' in user_input or ',' in user_input:
            raise InvalidIDException()

        try:
            int_id = int(user_input)
        except (TypeError, ValueError) as _:
            raise InvalidIDException()

        if int_id <= 0:
            raise InvalidIDException()
        return int_id

    def _convert_user_input_to_command(self, user_input):
        command = 'unknown'
        lowered_user_input = user_input.lower()
        for k, v in self._commands.items():
            if lowered_user_input in v:
                command = k
        return command

    def ask_command(self):
        user_input = self._console.input('Введите команду: ')
        converted = self._convert_user_input_to_command(user_input)
        return converted

    def ask_id(self):
        user_input = self._console.input('Введите ID пациента: ')
        converted = self._convert_str_user_input_to_int_id(user_input)
        return converted

    def answer_stop_app(self):
        self._console.print('Сеанс завершён.')

    def answer_patient_status(self, status):
        self._console.print(f'Статус пациента: "{status}"')

    def answer_patient_discharged(self):
        self._console.print('Пациент выписан из больницы')

    def answer_patient_status_changed(self, status):
        self._console.print(f'Новый статус пациента: "{status}"')

    def answer_patient_status_not_changed(self, status):
        self._console.print(f'Пациент остался в статусе "{status}"')

    def answer_got_unknown_command(self):
        self._console.print('Неизвестная команда! Попробуйте ещё раз')

    def answer(self, msg):
        self._console.print(msg)

    def ask_agreement_to_discharge_patient(self):
        user_input = self._console.input('Желаете этого клиента выписать? (да/нет): ')
        return user_input.lower() == 'да'
