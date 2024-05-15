from exceptions import UnknownIDException, StatusTooLowException


class HeadOfPatients:
    PATIENT_STATES = {
        0: "\"Тяжело болен\"",
        1: "\"Болен\"",
        2: "\"Слегка болен\"",
        3: "\"Готов к выписке\""
    }
    MAX_PATIENT_STATUS = 3
    MIN_PATIENT_STATUS = 0
    STATISTICS_HEAD = 'В больнице на данный момент находится {} чел., из них:'
    STATISTICS_LINE = '\t- в статусе {}: {} чел.'

    EMPTY_STATISTICS = 'В больнице на данный момент нет пациентов. Все вылечились :)'

    def __init__(self):
        self.patients = [1] * 200

    def has_patient(self, patient_id):
        try:
            self.patients[patient_id]
        except IndexError as ex:
            raise UnknownIDException()

    def get_status(self, patient_id):
        self.has_patient(patient_id)
        return self.PATIENT_STATES[self.patients[patient_id]]

    def status_down(self, patient_id):
        self.has_patient(patient_id)
        patient_status = self.patients[patient_id]
        if patient_status == self.MIN_PATIENT_STATUS:
            raise StatusTooLowException()
        else:
            self.patients[patient_id] -= 1
            return self.get_status(patient_id)

    def status_up(self, patient_id):
        self.has_patient(patient_id)
        self.patients[patient_id] += 1
        return self.get_status(patient_id)

    def discharge(self, patient_id):
        self.has_patient(patient_id)
        self.patients.pop(patient_id)

    def calculate_statistics(self):
        total_patients = len(self.patients)
        if total_patients:
            msg = ''
            msg += self.STATISTICS_HEAD.format(total_patients) + '\n'
            for status in set(self.patients):
                msg += self.STATISTICS_LINE.format(self.PATIENT_STATES[status], self.patients.count(status)) + '\n'
            return msg
        else:
            return self.EMPTY_STATISTICS

    def status_up_possible(self, patient_id):
        self.has_patient(patient_id)
        patient_status = self.patients[patient_id]
        if patient_status == self.MAX_PATIENT_STATUS:
            return False
        return True
