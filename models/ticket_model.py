from dataclasses import dataclass
from models.base_model import BaseModel
from enums.ticket_type import TicketType
"""
This module contains our main dataclass for Object Relational Mapping
"""

@dataclass
class ValidatedUserTicketInputs():
    priority: int
    ticket_type: TicketType
    title: str
    description: str
    initial_estimate: float
    
    """
    A dataclass representing the user input driven content of the Ticket model.
    It contains the following properties:
    - ticket_type: a TicketType enumeration value
    - name: a string representing the ticket name
    - description: a string describing the ticket
    - initial_estimate: a float representing the initial time estimate for the ticket
    - remaining_time: a float representing the remaining time to complete the ticket
    - logged_time: a float representing the time already spent on the ticket
    - priority: an integer between 1 and 5
    """

@dataclass
class TicketModel(ValidatedUserTicketInputs, BaseModel):
   #Combines BaseModel properties that all Models inherit with User Input fields from ValidatedUserTicketInputs and stores auto-calculated properties. 
    remaining_time: float
    logged_time: float

    def __post_init__(self):
        #self.ticket_type = TicketType(self.ticket_type)
        return super().__post_init__()


@dataclass
class ValidUpdateFields():
    priority: int
    ticket_type: TicketType
    title: str
    description: str

    