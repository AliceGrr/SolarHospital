from exceptions import PatientsNotExistsException, StatusTooLowException


class HeadOfPatients:
    _PATIENT_STATES = {
        0: "Тяжело болен",
        1: "Болен",
        2: "Слегка болен",
        3: "Готов к выписке"
    }
    _MAX_PATIENT_STATUS = 3
    _MIN_PATIENT_STATUS = 0
    _ID_OFFSET = 1

    def __init__(self, patients):
        self._patients = patients

    def _convert_id_to_index(self, patient_id):
        return patient_id-self._ID_OFFSET

    def _has_patient(self, patient_index):
        try:
            self._patients[patient_index]
        except IndexError as ex:
            raise PatientsNotExistsException()

    def get_status(self, patient_id):
        patient_index = self._convert_id_to_index(patient_id)
        self._has_patient(patient_index)
        return self._PATIENT_STATES[self._patients[patient_index]]

    def status_down(self, patient_id):
        patient_index = self._convert_id_to_index(patient_id)
        self._has_patient(patient_index)
        patient_status = self._patients[patient_index]
        if patient_status == self._MIN_PATIENT_STATUS:
            raise StatusTooLowException()
        else:
            self._patients[patient_index] -= 1

    def status_up(self, patient_id):
        patient_index = self._convert_id_to_index(patient_id)
        self._has_patient(patient_index)
        self._patients[patient_index] += 1

    def discharge(self, patient_id):
        patient_index = self._convert_id_to_index(patient_id)
        self._has_patient(patient_index)
        self._patients.pop(patient_index)

    def get_statistics(self):
        total_patients = len(self._patients)
        states_statistics = {self._PATIENT_STATES[state]: self._patients.count(state) for state in set(self._patients)}
        return total_patients, states_statistics

    def status_up_possible(self, patient_id):
        patient_index = self._convert_id_to_index(patient_id)
        self._has_patient(patient_index)
        patient_status = self._patients[patient_index]
        if patient_status == self._MAX_PATIENT_STATUS:
            return False
        return True
