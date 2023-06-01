from dataclasses import fields
from models.preview_model import TicketPreviewModel
from repositories.ticket_repository import TicketRepository
from models.ticket_model import TicketModel, ValidUpdateFields, ValidatedUserTicketInputs
from datetime import datetime
from services.base_service import BaseService


class TicketService(BaseService[TicketModel]):
    def __init__(self, ticket_repository: TicketRepository):
        super().__init__(ticket_repository)
        self.ticket_repository = ticket_repository
        
    def build_ticket(self, validated_inputs: ValidatedUserTicketInputs) -> TicketModel:
        """
        Create a new ticket based on validated user inputs and automatically calculated properties.

        Args:
            validated_inputs (ValidatedUserTicketInputs): The validated inputs for the new ticket.

        Returns:
            TicketModel: The new ticket.
        """
        return TicketModel(
            id=None,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            completed=False,
            deleted=False,
            priority=validated_inputs.priority,
            ticket_type=validated_inputs.ticket_type,
            title=validated_inputs.title,
            description=validated_inputs.description,
            initial_estimate=validated_inputs.initial_estimate,
            remaining_time=validated_inputs.initial_estimate,
            logged_time=0.0 
        )
    
    def create_ticket(self, validated_inputs) -> TicketModel:
        return self.ticket_repository.add_to_db(self.build_ticket(validated_inputs))
    
    def create_preview(self, tickets: list[TicketModel]) -> list[TicketPreviewModel]:
        return [TicketPreviewModel(t.id, t.priority, t.title, t.remaining_time) for t in tickets]
       
    def order_by_priority(self, tickets: list[TicketModel]) -> list[TicketModel]:
        """
        Went for a count sort here as we already know the values we are sorting (1-5)
        Create a list for each priority number, iterate over tickets store by priority as index, re-join the list.
        """
        buckets = [[] for _ in range(5)]

        for t in tickets:
            buckets[t.priority - 1].append(t)

        sorted_buckets = [self.sort_remaining_time(bucket) for bucket in buckets]

        return [ticket for bucket in sorted_buckets for ticket in bucket]
    
    def sort_remaining_time(self, tickets: list[TicketModel]):
        """
        Very Basic Quick Sort Algorithm to order by remaining time.

        QS is recursive, so we have our exit case immediately.

        Split our list into a left/right where remaining time is less/greater than the middle element.

        Recursively call on each list until sorted.

        TODO: This is a basic, memory inefficient implementation, revisit later.
        """
        if len(tickets) <= 1:
            return tickets
        
        pivot = tickets[len(tickets) // 2]

        left = [lower for lower in tickets if (lower.remaining_time < pivot.remaining_time)] 
        middle = [ticket for ticket in tickets if ticket.remaining_time == pivot.remaining_time]
        right = [greater for greater in tickets if (greater.remaining_time > pivot.remaining_time)]

        return self.sort_remaining_time(left) + middle + self.sort_remaining_time(right)
    
    def search_string_values(self, tickets: list[TicketModel], query: str):
        return [t for t in tickets if query.upper() in (t.title.upper() or t.description.upper())]

    def delete_record(self, id: int) -> TicketModel:
        return self.ticket_repository.delete_record(id, datetime.now())
    
    def populate_update_fields(self, ticket: TicketModel) -> ValidUpdateFields:
        data = {f.name: getattr(ticket, f.name) for f in fields(ValidUpdateFields)}
        return ValidUpdateFields(**data)

    def check_ticket_in_progress(self, ticket: TicketModel) -> bool:
        return ticket.logged_time > 0
    
    def update_record(self, ticket: TicketModel, field_to_update: int, updated_value) -> TicketModel:
        setattr(ticket, [f.name for f in fields(ValidUpdateFields)][field_to_update - 1], updated_value)
        self.ticket_repository.update_record(ticket.id, ticket, datetime.now())

    def log_time(self, ticket: TicketModel, time):
        
        true_remaining_time = ticket.remaining_time - time
        true_time_logged = ticket.logged_time + time

        updated_ticket = self.ticket_repository.log_time(ticket.id, true_remaining_time, true_time_logged, datetime.now())

        if (updated_ticket.remaining_time <= 0):
            self.ticket_repository.complete_record(ticket.id, datetime.now())
        
        return updated_ticket

        