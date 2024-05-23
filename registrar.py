from coordinator import Coordinator
from translator import Translator


class Registrar:
    def __init__(self):
        self._translator = Translator()
        self._coordinator = Coordinator(self._translator)

    def start(self):
        while True:
            command = self._translator.ask_command()
            match command:
                case 'stop':
                    self._translator.answer_stop()
                    break
                case 'status_up':
                    self._coordinator.status_up()
                case 'get_status':
                    self._coordinator.get_status()
                case 'calculate_statistics':
                    self._coordinator.calculate_statistics()
                case _:
                    self._translator.answer_unknown_command()

