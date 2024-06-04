class Hospital:
    def __init__(self, dialog_with_user, coordinator):
        self._dialog_with_user = dialog_with_user
        self._coordinator = coordinator

    def start(self):
        while True:
            command = self._dialog_with_user.ask_command()
            match command:
                case 'stop':
                    self._dialog_with_user.answer_stop_app()
                    break
                case 'status_up':
                    self._coordinator.status_up()
                case 'get_status':
                    self._coordinator.get_status()
                case 'calculate_statistics':
                    self._coordinator.calculate_statistics()
                case 'status_down':
                    self._coordinator.status_down()
                case 'discharge':
                    self._coordinator.discharge()
                case 'unknown':
                    self._dialog_with_user.answer_got_unknown_command()
