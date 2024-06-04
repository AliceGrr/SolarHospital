from exceptions import InvalidIDException, PatientsNotExistsException, StatusTooHighException, StatusTooLowException


class Coordinator:

    def __init__(self, translator, head_of_patients):
        self._translator = translator
        self._head_of_patients = head_of_patients

    def status_up(self):
        try:
            patient_id = self._translator.ask_id()
            if self._head_of_patients.status_up_possible(patient_id):
                self._head_of_patients.status_up(patient_id)
                status = self._head_of_patients.get_status(patient_id)
                self._translator.answer_patient_status_changed(status)
            else:
                agreement = self._translator.ask_agreement_to_discharge_patient()
                if agreement:
                    self._head_of_patients.discharge(patient_id)
                    self._translator.answer_patient_discharged()
                else:
                    status = self._head_of_patients.get_status(patient_id)
                    self._translator.answer_patient_status_not_changed(status)
        except (PatientsNotExistsException, InvalidIDException, StatusTooHighException) as ex:
            self._translator.answer(ex.message)

    def get_status(self):
        try:
            patient_id = self._translator.ask_id()
            status = self._head_of_patients.get_status(patient_id)
            self._translator.answer_patient_status(status)
        except (InvalidIDException, PatientsNotExistsException) as ex:
            self._translator.answer(ex.message)

    def calculate_statistics(self):
        total_patients, statistics = self._head_of_patients.get_statistics()
        if total_patients:
            msg = ''
            msg += f'В больнице на данный момент находится {total_patients} чел., из них:\n'
            for status, count in statistics.items():
                msg += f'\t- в статусе "{status}": {count} чел.\n'
            self._translator.answer(msg)
        else:
            self._translator.answer('В больнице на данный момент нет пациентов. Все вылечились :)')

    def status_down(self):
        try:
            patient_id = self._translator.ask_id()
            self._head_of_patients.status_down(patient_id)
            status = self._head_of_patients.get_status(patient_id)
            self._translator.answer_patient_status_changed(status)
        except (InvalidIDException, PatientsNotExistsException, StatusTooLowException) as ex:
            self._translator.answer(ex.message)

    def discharge(self):
        try:
            patient_id = self._translator.ask_id()
            self._head_of_patients.discharge(patient_id)
            self._translator.answer_patient_discharged()
        except (InvalidIDException, PatientsNotExistsException) as ex:
            self._translator.answer(ex.message)
