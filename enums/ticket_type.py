from enum import Enum

"""
This module contains the TicketType enumeration for representing the valid ticket types.
"""


# I opted for this as a method of statically stored Constants
# due to the limitations of a single table Database
class TicketType(Enum):
    """
    An enumeration to represent our three valid Ticket Types
    1: DEVELOPMENT
    2: TESTING
    3: DEPLOYMENT
    """
    PLANNING = 'PLANNING'
    DESIGN = 'DESIGN'
    DEVELOPMENT = 'DEVELOPMENT'
    TESTING = 'TESTING'
    DEPLOYMENT = 'DEPLOYMENT'
    DOCUMENTATION = 'DOCUMENTATION'
    SUPPORT = 'SUPPORT'
