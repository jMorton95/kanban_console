from controllers.ticket_controller import TicketController
from repositories.database_connection import DatabaseConnection
from repositories.ticket_repository import TicketRepository
from services.tickets.ticket_input_validation_service import TicketInputValidationService
from services.terminal.output_manager import OutputManager
from services.terminal.formatter import Formatter
from services.terminal.output_manager import PromptManager

from services.tickets.ticket_service import TicketService
from environment.env import DB_TICKET_STRING

class Configuration():
    def __init__(self):
        self.app_db_conn = DatabaseConnection()
        self.output_manager = OutputManager(
            Formatter(),
            PromptManager(),
        )

class TicketConfiguration(Configuration):
    def __init__(self):
        super().__init__()

    def compose_ticket_controller(self) -> TicketController:
        return TicketController(
            TicketService(
                TicketRepository(
                    self.app_db_conn,
                    DB_TICKET_STRING,
                )
            ),
            TicketInputValidationService(),
            self.output_manager,
        )
        
