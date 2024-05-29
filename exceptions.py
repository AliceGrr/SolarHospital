class PatientsNotExistsException(Exception):
    message = 'Ошибка. В больнице нет пациента с таким ID'


class InvalidIDException(Exception):
    message = 'Ошибка. ID пациента должно быть числом (целым, положительным)'

class StatusTooLowException(Exception):
    message = 'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)'

