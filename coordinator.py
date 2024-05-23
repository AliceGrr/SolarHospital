from exceptions import InvalidIDException, UnknownIDException
from head_of_patients import HeadOfPatients


class Coordinator:
    _STATISTICS_HEAD = 'В больнице на данный момент находится {} чел., из них:'
    _STATISTICS_LINE = '\t- в статусе "{}": {} чел.'

    _EMPTY_STATISTICS = 'В больнице на данный момент нет пациентов. Все вылечились :)'

    def __init__(self, translator):
        self._translator = translator
        self._head_of_patients = HeadOfPatients()

    def status_up(self):
        try:
            patient_id = self._translator.ask_id()
            if self._head_of_patients.status_up_possible(patient_id):
                self._head_of_patients.status_up(patient_id)
                status = self._head_of_patients.get_status(patient_id)
                self._translator.answer_status_changed(status)
            else:
                agreement = self._translator.ask_agreement()
                if agreement:
                    self._head_of_patients.discharge(patient_id)
                    self._translator.answer_discharged()
                else:
                    status = self._head_of_patients.get_status(patient_id)
                    self._translator.answer_status_not_changed(status)
        except UnknownIDException as ex:
            self._translator.answer_exception(ex)
        except InvalidIDException as ex:
            self._translator.answer_exception(ex)

    def get_status(self):
        try:
            patient_id = self._translator.ask_id()
            status = self._head_of_patients.get_status(patient_id)
            self._translator.answer_status(status)
        except InvalidIDException as ex:
            self._translator.answer_exception(ex)
        except UnknownIDException as ex:
            self._translator.answer_exception(ex)

    def calculate_statistics(self):
        total_patients, statistics = self._head_of_patients.get_statistics()
        if total_patients:
            msg = ''
            msg += self._STATISTICS_HEAD.format(total_patients) + '\n'
            for status, count in statistics.items():
                msg += self._STATISTICS_LINE.format(status, count) + '\n'
            self._translator.answer(msg)
        else:
            self._translator.answer(self._EMPTY_STATISTICS)
