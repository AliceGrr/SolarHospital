from constants import Messages, ID_OFFSET, PATIENT_STATES, MIN_PATIENT_STATUS, MAX_PATIENT_STATUS, AGREE
from exceptions import UnknownCommandException, StopException, UnknownIDException, InvalidIDException, TooLowIDException


class Hospital:
    def __init__(self):
        self.patients = [1]*200
        self.commands_without_params = [self.stop, self.calculate_statistics]
        self.commands = {
            self.get_status: ('get status', 'узнать статус пациента'),
            self.status_up: ('status up', 'повысить статус пациента'),
            self.status_down: ('status down', 'понизить статус пациента'),
            self.discharge: ('discharge', 'выписать пациента'),
            self.calculate_statistics: ('calculate statistics', 'рассчитать статистику'),
            self.stop: ('stop', 'стоп')
        }

    def start(self):
        while True:
            try:
                command = self.validate_command_input(input(Messages.ENTER_COMMAND))
                if command in self.commands_without_params:
                    command()
                else:
                    patient_id = self.validate_id_input(input(Messages.ENTER_ID))
                    command(patient_id-ID_OFFSET)
            except StopException as ex:
                print(Messages.STOP)
                break
            except TooLowIDException as ex:
                print(Messages.STATUS_TOO_LOW)
            except UnknownIDException as ex:
                print(Messages.UNKNOWN_ID)
            except UnknownCommandException as ex:
                print(Messages.UNKNOWN_COMMAND)
            except InvalidIDException as ex:
                print(Messages.INVALID_ID)
            except Exception as ex:
                print('Unexpected error:', ex)

    def validate_id_input(self, user_input):
        total_patients = len(self.patients)

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

        if int_id <= total_patients:
            return int_id
        raise UnknownIDException()

    def validate_command_input(self, user_input):
        command = None
        lowered_user_input = user_input.lower()
        for k, v in self.commands.items():
            if lowered_user_input in v:
                command = k
        if not command:
            raise UnknownCommandException()
        return command

    def get_status(self, patient_id):
        print(PATIENT_STATES[self.patients[patient_id]])

    def status_down(self, patient_id):
        patient_status = self.patients[patient_id]
        if patient_status == MIN_PATIENT_STATUS:
            raise TooLowIDException()
        else:
            self.patients[patient_id] -= 1
            print(Messages.NEW_PATIENT_STATUS.format(PATIENT_STATES[self.patients[patient_id]]))

    def status_up(self, patient_id):
        patient_status = self.patients[patient_id]
        if patient_status == MAX_PATIENT_STATUS:
            agree = input(Messages.DISCHARGE_REQUEST)
            if agree.lower() == AGREE:
                self.discharge(patient_id)
            else:
                print(Messages.PATIENT_STATUS_NOT_CHANGED.format(PATIENT_STATES[patient_status]))
        else:
            self.patients[patient_id] += 1
            print(Messages.NEW_PATIENT_STATUS.format(PATIENT_STATES[self.patients[patient_id]]))

    def discharge(self, patient_id):
        self.patients.pop(patient_id)
        print(Messages.PATIENT_DISCHARGED)

    def calculate_statistics(self):
        total_patients = len(self.patients)
        if total_patients:
            print(Messages.STATISTICS_HEAD.format(total_patients))
            for status in set(self.patients):
                print(Messages.STATISTICS_LINE.format(PATIENT_STATES[status], self.patients.count(status)))
        else:
            print(Messages.EMPTY_STATISTICS)

    def stop(self):
        raise StopException()
