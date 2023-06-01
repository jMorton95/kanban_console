from services.tickets.ticket_input_validation_service import TicketInputValidationService
from services.terminal.output_manager import OutputManager
from services.tickets.ticket_service import TicketService

class TicketController():
    def __init__(self, ticket_service: TicketService, ticket_input_validator: TicketInputValidationService, output_manager: OutputManager):
        self.service = ticket_service
        self.input_validator = ticket_input_validator
        self.output_manager = output_manager
        self.commands = {
            1: self.preview_all,
            2: self.view_by_id,
            3: self.new_ticket,
            4: self.update_ticket,
            5: self.delete_ticket,
            6: self.search_by_name,
            7: self.show_deleted,
            8: self.show_all_raw,
            9: self.quit
        }
    

    def start(self):
        run = True
        while run:
            user_command = self.output_manager.startup_message(
                not_deleted = len(self.service.filter_deleted(False, self.service.get_all())),
                outstanding = len(self.service.filter_deleted(False, self.service.filter_complete(False, self.service.get_all())))
            )

            run = self.commands[user_command]()
            if run:
                self.output_manager.prompt_manager.continue_message() 

    def command(self, command: int):
        self.commands[command]()

    def preview_all(self):
        non_deleted_tickets = self.service.filter_deleted(False, self.service.get_all())
        ordered_non_deleted_tickets = self.service.order_by_priority(non_deleted_tickets)
        preview = self.service.create_preview(ordered_non_deleted_tickets)
        self.output_manager.single_line(preview)
        return True

    def view_by_id(self):
        id = self.output_manager.get_id_input(self.service.get_count())
        ticket = self.service.get_by_id(id)

        if (self.service.check_if_deleted(ticket)):
            self.output_manager.no_records_found(f"Record deleted. {ticket.updated_date}")
            return True

        self.output_manager.multi_line(ticket)

        if (self.service.check_if_completed(ticket)):
            return True

        if self.output_manager.prompt_manager.get_user_confirmation("log time to ticket:", id):
            time_to_log = self.output_manager.display_time_logging_information(ticket.remaining_time)
            self.service.log_time(ticket, time_to_log)

        return True

    def new_ticket(self):
        ticket = self.service.create_ticket(self.input_validator.generate_validated_user_ticket_inputs())
        self.output_manager.single_line(ticket)
        return True

    def update_ticket(self):
        selected_ticket = self.service.get_by_id(self.output_manager.get_id_input(self.service.get_count()))

        if (self.service.check_if_deleted(selected_ticket)):
            self.output_manager.no_records_found(f"Record deleted. {selected_ticket.updated_date}")
        else:
            field_to_update = self.output_manager.display_update_information(self.service.populate_update_fields(selected_ticket))
            updated_value = self.input_validator.call_chosen_update_function(field_to_update)

            self.service.update_record(selected_ticket, field_to_update, updated_value)
        return True
        
    def delete_ticket(self):
        id = self.output_manager.get_id_input(self.service.get_count())
        record = self.service.get_by_id(id)
        if (record.deleted):
            print_red("Record already deleted. ")
            return
        
        self.output_manager.single_line(record)
        
        if (self.output_manager.prompt_manager.get_user_confirmation("delete record", id)):
            self.output_manager.multi_line(self.service.delete_record(id))

        return True

    def search_by_name(self):
        ticket = self.service.get_all()
        filtered = self.service.search_string_values(ticket, self.output_manager.prompt_manager.get_raw_string_from_user())
        self.output_manager.multi_line(filtered)
        return True

    def show_deleted(self):
        deleted = self.service.filter_deleted(True, self.service.get_all())
        preview = self.service.create_preview(deleted)
        self.output_manager.single_line(preview)
        return True

    def show_all_raw(self):
        self.output_manager.multi_line(self.service.get_all())
        return True

    def quit(self):
        return self.output_manager.prompt_manager.get_user_confirmation("quit the application")
         


