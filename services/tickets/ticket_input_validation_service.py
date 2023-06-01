from enums.ticket_type import TicketType
from models.ticket_model import ValidatedUserTicketInputs
from functools import partial

class TicketInputValidationService:
    """
    The TicketInputValidationService class handles user input and validation for ticket attributes.
    """

    def __init__(self):
        self.commands = {
            1: self.prompt_and_validate_priority,
            2: self.prompt_and_validate_ticket_type,
            3: partial(self.prompt_for_string_of_minimum_length, length=10),
            4: partial(self.prompt_for_string_of_minimum_length, length=25),
        }

    def prompt_and_validate_priority(self) -> int:
        """
        Prompt the user for a ticket priority and validate it. 
        The valid priority values are between 1 and 5 (inclusive).

        Returns:
            int: The validated ticket priority.
        """

        MIN_PRIORITY = 1
        MAX_PRIORITY = 5

        while True:
            user_input = input("Please enter a Priority between 1 & 5, or 'Exit' to stop. ")

            if (user_input.upper == "EXIT"):
                break

            try:
                priority = int(user_input)
            except ValueError:
                print(f"{user_input} is not a number. ")
                continue

            if not (priority >= MIN_PRIORITY and priority <= MAX_PRIORITY):
                print(f"{user_input} is not between {MIN_PRIORITY} and {MAX_PRIORITY}. ")
                continue
            
            return priority
    
    def prompt_and_validate_ticket_type(self) -> TicketType:
        """
        Prompt the user for a ticket type and validate it.
        The valid ticket types are the names of the TicketType enum values.

        Returns:
            TicketType: The validated ticket type.
        """

        while True:
            user_input = input(f"Please enter a ticket type. Valid Options: {', '.join([i.name for i in TicketType])} ")

            try: 
                ticket_type = TicketType[user_input.upper()]
            except KeyError:
                print(f"{user_input} is not a valid Ticket Type. ")
                continue

            return ticket_type
        
    def prompt_for_string_of_minimum_length(self, prompt: str, length: int) -> str:
        """
        Prompt the user for a string and validate that its length is greater than or equal to the given length.

        Args:
            prompt (str): The prompt message to display to the user.
            length (int): The minimum valid string length.

        Returns:
            str: The validated string.
        """

        while True:
            user_input = input(f"Please enter a {prompt} longer than {length} character{'s' if length > 1 else ''} ")

            if not (len(user_input) >= length):
                print(f"'{user_input}' is not longer than {length} character{'s' if length > 1 else ''} ")
                continue
            else:
                return user_input
            
    def prompt_for_initial_estimate(self) -> float:
        """
        Prompt the user for an initial estimate of hours and validate it.
        The estimate is given as a float (e.g. '5.5' = 5h30m).

        Returns:
            float: The validated initial estimate.
        """

        while True:
            user_input = input(f"Please enter an initial estimate of hours/minutes as a Float (e.g. '5.5' = 5h30m). ")

            try:
                estimate = float(user_input)
            except ValueError:
                print(f"{user_input} was not a valid number. ")
                continue

            return estimate

    def generate_validated_user_ticket_inputs(self) -> ValidatedUserTicketInputs:
        """
        Generate a ValidatedUserTicketInputs object with user input values.
        Each attribute of the object is prompted and validated.

        Returns:
            ValidatedUserTicketInputs: The validated user ticket inputs.
        """

        return ValidatedUserTicketInputs(
            self.prompt_and_validate_priority(),
            self.prompt_and_validate_ticket_type(),
            self.prompt_for_string_of_minimum_length('Ticket Name', 10),
            self.prompt_for_string_of_minimum_length('Ticket Description', 25),
            self.prompt_for_initial_estimate()
        )
    
    def call_chosen_update_function(self, choice: int):
        return self.commands[choice]()