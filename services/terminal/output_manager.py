import dataclasses
from helpers.extension_helpers import check_option_in_range, find_option_by_number, validate_as_int
from helpers.print_colours import print_beige, print_blue, print_green, print_red, print_yellow, prompt_underline
from services.terminal.formatter import Formatter
from services.terminal.prompt_manager import PromptManager


class OutputManager:

    def __init__(self, formatter: Formatter, prompt_manager: PromptManager):
        self.formatter = formatter
        self.prompt_manager = prompt_manager

    start_options = [
        "1: View All Records",
        "2: View Record by ID", "3: Add a new Record",
        "4: Update by ID", "5: Delete by ID",
        "6: Search for Records",
        "7: Show deleted records.",
        "8: Show all data raw & unfiltered.",
        "9: Quit"
    ]

    update_options = [
        "1: Priority",
        "2: Ticket Type",
        "3: Title",
        "4: Description"
    ]
    
    def _print_single_line(self, obj, colour_func):
        colour_func(' '.join(self.formatter.format_object(obj)))

    def _print_multi_line(self, obj, colour_func):
        for entry in self.formatter.format_object(obj):
            colour_func(entry)

    def _handle_print(self, objects: list, single_line: bool):
        #This is designed to let you call 'multi_line' or 'single_line' in our controller without having to care what format the data looks like.
        #We can pass a single object or a list of any length without having to validate it at the caller level.
        #Using the strategy pattern throughout to decide the behaviour at runtime.
        print_func = self._print_single_line if single_line else self._print_multi_line

        if not isinstance(objects, list):
            objects = [objects]

        if len(objects) <= 0:
            self.no_records_found()

        for obj in objects:
            #Print in yellow for even, beige for odd indexes.
            colour_func = print_yellow if (objects.index(obj) % 2 == 0) else print_beige
            print_func(obj, colour_func)

    def multi_line(self, objects: list):
        self._handle_print(objects, single_line=False)

    def single_line(self, objects: list):
        self._handle_print(objects, single_line=True)

    def startup_message(self, not_deleted: int, outstanding: int):
        print_green(f"Welcome to Kanban_Console, there are {outstanding} outstanding tickets, and {not_deleted} in total!\n")
        self.print_options(self.start_options)
        return self.prompt_manager.get_user_choice(self.start_options)

    def no_records_found(self, optional: str | None = None):
        print_red("No records found.")
        if (optional): print_red(optional)

    def print_options(self, options):
        for opt in options:
            print_blue(opt)

    def get_id_input(self, range: int):
        return self.prompt_manager.get_number_from_user_in_range(range)
    
    def display_update_information(self, items):
        self.multi_line(items)
        print_green("Please note, once a ticket has been created, the initial estimate cannot be changed.\nPlease open a record by ID to log time. ")
        self.print_options(self.update_options)
        return self.prompt_manager.get_number_from_user_in_range(len(self.update_options))
    
    def display_time_logging_information(self, remaining_time: float):
        print_green(f"Available time: {remaining_time}")
        time_to_log = self.prompt_manager.get_number_from_user_in_range(remaining_time)
        if time_to_log == remaining_time:
            print_green("Ticket now complete. ")
        return time_to_log
