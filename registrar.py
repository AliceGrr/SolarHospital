from coordinator import Coordinator
from exceptions import InvalidIDException
from translator import Translator


class Registrar:
    def __init__(self):
        self.translator = Translator()
        self.coordinator = Coordinator(self.translator)

    def start(self):
        while True:
            try:
                command = self.translator.ask_command()
            except InvalidIDException as ex:
                self.translator.answer_exception(ex)
            else:
                if not command:
                    self.translator.answer_unknown_command()
                elif command == 'stop':
                    self.translator.answer_stop()
                    break
                else:
                    self.coordinator.call_worker(command)

