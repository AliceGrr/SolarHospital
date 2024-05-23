from exceptions import InvalidIDException


class Messages:
    AGREE = 'да'
    ENTER_COMMAND = 'Введите команду: '
    ENTER_ID = 'Введите ID пациента: '

    PATIENT_STATUS = 'Статус пациента: "{}"'
    NEW_PATIENT_STATUS = 'Новый статус пациента: "{}"'
    PATIENT_STATUS_NOT_CHANGED = 'Пациент остался в статусе "{}"'

    DISCHARGE_REQUEST = 'Желаете этого клиента выписать? (да/нет): '

    PATIENT_DISCHARGED = 'Пациент выписан из больницы'

    STOP = 'Сеанс завершён.'

    UNKNOWN_COMMAND = 'Неизвестная команда! Попробуйте ещё раз'


class Translator:
    _ID_OFFSET = 1

    def __init__(self):
        self._commands = {
            'get_status': ('get status', 'узнать статус пациента'),
            'status_up': ('status up', 'повысить статус пациента'),
            'status_down': ('status down', 'понизить статус пациента'),
            'discharge': ('discharge', 'выписать пациента'),
            'calculate_statistics': ('calculate statistics', 'рассчитать статистику'),
            'stop': ('stop', 'стоп')
        }

    def _validate_and_translate_id_input(self, user_input):
        if '.' in user_input or ',' in user_input:
            raise InvalidIDException()

        try:
            int_id = int(user_input)
        except TypeError as ex:
            raise InvalidIDException()
        except ValueError as ex:
            raise InvalidIDException()

        if int_id <= 0:
            raise InvalidIDException()
        return int_id-self._ID_OFFSET

    def _translate_command_input(self, user_input):
        command = None
        lowered_user_input = user_input.lower()
        for k, v in self._commands.items():
            if lowered_user_input in v:
                command = k
        return command

    def ask_command(self):
        user_input = input(Messages.ENTER_COMMAND)
        translated = self._translate_command_input(user_input)
        return translated

    def ask_id(self):
        user_input = input(Messages.ENTER_ID)
        translated = self._validate_and_translate_id_input(user_input)
        return translated

    def answer_stop(self):
        print(Messages.STOP)

    def answer_status(self, status):
        print(Messages.PATIENT_STATUS.format(status))

    def answer_discharged(self):
        print(Messages.PATIENT_DISCHARGED)

    def answer_status_changed(self, status):
        print(Messages.NEW_PATIENT_STATUS.format(status))

    def answer_status_not_changed(self, status):
        print(Messages.PATIENT_STATUS_NOT_CHANGED.format(status))

    def answer_status_too_low(self):
        print(Messages.STATUS_TOO_LOW)

    def answer_unknown_command(self):
        print(Messages.UNKNOWN_COMMAND)

    def answer_exception(self, ex):
        print(ex.message)

    def answer(self, msg):
        print(msg)

    def ask_agreement(self):
        user_input = input(Messages.DISCHARGE_REQUEST)
        if user_input.lower() == Messages.AGREE:
            return True
