from coordinator import Coordinator
from head_of_patients import HeadOfPatients
from registrar import Registrar
from translator import Translator


if __name__ == '__main__':
    patients = [1] * 200
    head_of_patients = HeadOfPatients(patients)
    translator = Translator()
    coordinator = Coordinator(translator, head_of_patients)
    registrar = Registrar(translator, coordinator)
    registrar.start()

