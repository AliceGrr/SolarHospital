class MockConsole:
    def __init__(self):
        self.output_messages = []
        self.requests_and_responses = []

    def input(self, input_message):
        assert self.requests_and_responses, f"{input_message} not in {self.requests_and_responses}"
        assert input_message in self.requests_and_responses[0], f"{input_message} is not {self.requests_and_responses[0]}, full list: {self.requests_and_responses}"

        return self.requests_and_responses.pop(0).pop(input_message)

    def print(self, output_message):
        assert self.output_messages, f"{output_message} not in {self.output_messages}"
        assert output_message == self.output_messages[0], f"{output_message} is not {self.output_messages[0]}, full list: {self.output_messages}"

        self.output_messages.remove(output_message)

    def add_expected_request_and_response(self, input_message, user_input):
        self.requests_and_responses.append({input_message: user_input})

    def add_expected_output_message(self, output_message):
        self.output_messages.append(output_message)

    def verify_all_calls_have_been_made(self):
        assert not self.output_messages, f"output messages list is not empty: {self.output_messages}"
        assert not self.requests_and_responses, f"requests and responses dict is not empty: {self.output_messages}"
