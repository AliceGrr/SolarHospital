from coordinator import Coordinator
from head_of_patients import HeadOfPatients
from hospital import Hospital
from dialog_with_user import DialogWithUser


if __name__ == '__main__':
    patients = [1] * 200
    head_of_patients = HeadOfPatients(patients)
    translator = DialogWithUser()
    coordinator = Coordinator(translator, head_of_patients)
    hospital = Hospital(translator, coordinator)
    hospital.start()

