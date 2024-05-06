PATIENT_STATES = {
    0: "\"Тяжело болен\"",
    1: "\"Болен\"",
    2: "\"Слегка болен\"",
    3: "\"Готов к выписке\""
}
ID_OFFSET = 1
MAX_PATIENT_STATUS = 3
MIN_PATIENT_STATUS = 0
AGREE = 'да'


class Messages:
    ENTER_COMMAND = 'Введите команду: '
    ENTER_ID = 'Введите ID пациента: '

    PATIENT_STATUS = 'Статус пациента: {}'
    NEW_PATIENT_STATUS = 'Новый статус пациента: {}'
    PATIENT_STATUS_NOT_CHANGED = 'Пациент остался в статусе {}'

    DISCHARGE_REQUEST = 'Желаете этого клиента выписать? (да/нет): '

    PATIENT_DISCHARGED = 'Пациент выписан из больницы'

    STATISTICS_HEAD = 'В больнице на данный момент находится {} чел., из них:'
    STATISTICS_LINE = '\t- в статусе {}: {} чел.'

    EMPTY_STATISTICS = 'В больнице на данный момент нет пациентов. Все вылечились :)'

    STOP = 'Сеанс завершён.'

    STATUS_TOO_LOW = 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'

    UNKNOWN_COMMAND = 'Неизвестная команда! Попробуйте ещё раз'
    UNKNOWN_ID = 'Ошибка. В больнице нет пациента с таким ID'
    INVALID_ID = 'Ошибка. ID пациента должно быть числом (целым, положительным)'


