from exceptions import InvalidIDException, UnknownIDException, StatusTooLowException
from head_of_patients import HeadOfPatients


class Coordinator:
    def __init__(self, translator):
        self.translator = translator
        self.head_of_patients = HeadOfPatients()
        self.commands_without_params = ['calculate_statistics']

        self.commands = {
            'get_status': self.head_of_patients.get_status,
            'status_up': self.status_up,
            'status_down': self.head_of_patients.status_down,
            'discharge': self.head_of_patients.discharge,
            'calculate_statistics': self.head_of_patients.calculate_statistics,
        }

        self.complex_commands = ['status_up']

        self.answers = {
            'get_status': self.translator.answer_status,
            'status_down': self.translator.answer_status_changed,
            'discharge': self.translator.answer_discharged,
            'calculate_statistics': self.translator.answer,
        }

    def status_up(self):
        patient_id = self.translator.ask_id()
        if self.head_of_patients.status_up_possible(patient_id):
            status = self.head_of_patients.status_up(patient_id)
            self.translator.answer_status_changed(status)
        else:
            agreement = self.translator.ask_agreement()
            if agreement:
                self.head_of_patients.discharge(patient_id)
                self.translator.answer_discharged()
            else:
                status = self.head_of_patients.get_status(patient_id)
                self.translator.answer_status_not_changed(status)

    def call_worker(self, command):
        try:
            if command in self.complex_commands:
                self.commands[command]()
            else:
                if command in self.commands_without_params:
                    answer_data = self.commands[command]()
                else:
                    patient_id = self.translator.ask_id()
                    answer_data = self.commands[command](patient_id)

                if answer_data:
                    self.answers[command](answer_data)
                else:
                    self.answers[command]()

        except InvalidIDException as ex:
            self.translator.answer_exception(ex)
        except UnknownIDException as ex:
            self.translator.answer_exception(ex)
        except StatusTooLowException as ex:
            self.translator.answer_exception(ex)


