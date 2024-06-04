from exceptions import InvalidIDException, PatientsNotExistsException, StatusTooHighException, StatusTooLowException


class Coordinator:

    def __init__(self, dialog_with_user, head_of_patients):
        self._dialog_with_user = dialog_with_user
        self._head_of_patients = head_of_patients

    def status_up(self):
        try:
            patient_id = self._dialog_with_user.ask_id()
            if self._head_of_patients.status_up_possible(patient_id):
                self._head_of_patients.status_up(patient_id)
                status = self._head_of_patients.get_status(patient_id)
                self._dialog_with_user.answer_patient_status_changed(status)
            else:
                agreement = self._dialog_with_user.ask_agreement_to_discharge_patient()
                if agreement:
                    self._head_of_patients.discharge(patient_id)
                    self._dialog_with_user.answer_patient_discharged()
                else:
                    status = self._head_of_patients.get_status(patient_id)
                    self._dialog_with_user.answer_patient_status_not_changed(status)
        except (PatientsNotExistsException, InvalidIDException, StatusTooHighException) as ex:
            self._dialog_with_user.answer(ex.message)

    def get_status(self):
        try:
            patient_id = self._dialog_with_user.ask_id()
            status = self._head_of_patients.get_status(patient_id)
            self._dialog_with_user.answer_patient_status(status)
        except (InvalidIDException, PatientsNotExistsException) as ex:
            self._dialog_with_user.answer(ex.message)

    def make_string_statistics(self, total_patients, statistics):
        if total_patients:
            msg = ''
            msg += f'В больнице на данный момент находится {total_patients} чел., из них:\n'
            for status, count in statistics.items():
                msg += f'\t- в статусе "{status}": {count} чел.\n'
            return msg
        else:
            return 'В больнице на данный момент нет пациентов. Все вылечились :)'

    def calculate_statistics(self):
        total_patients, statistics = self._head_of_patients.get_statistics()
        msg = self.make_string_statistics(total_patients, statistics)
        self._dialog_with_user.answer(msg)

    def status_down(self):
        try:
            patient_id = self._dialog_with_user.ask_id()
            self._head_of_patients.status_down(patient_id)
            status = self._head_of_patients.get_status(patient_id)
            self._dialog_with_user.answer_patient_status_changed(status)
        except (InvalidIDException, PatientsNotExistsException, StatusTooLowException) as ex:
            self._dialog_with_user.answer(ex.message)

    def discharge(self):
        try:
            patient_id = self._dialog_with_user.ask_id()
            self._head_of_patients.discharge(patient_id)
            self._dialog_with_user.answer_patient_discharged()
        except (InvalidIDException, PatientsNotExistsException) as ex:
            self._dialog_with_user.answer(ex.message)
