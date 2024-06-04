from console import Console
from coordinator import Coordinator
from head_of_patients import HeadOfPatients
from hospital import Hospital
from dialog_with_user import DialogWithUser


if __name__ == '__main__':
    patients = [1] * 200
    head_of_patients = HeadOfPatients(patients)
    console = Console()
    dialog_with_user = DialogWithUser(console)
    coordinator = Coordinator(dialog_with_user, head_of_patients)
    hospital = Hospital(dialog_with_user, coordinator)
    hospital.start()

