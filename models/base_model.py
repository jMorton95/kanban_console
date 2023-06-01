from dataclasses import dataclass
from datetime import datetime
from typing import Optional

"""
This module contains our Base database Model.
Every dataclass we instantiate will inherit from this.
"""

@dataclass 
class BaseModel:
    """
    A dataclass representing common properties every Model in the application will inherit.

    id: an integer Unique Identifier that will be auto-generated on record creation.
    created_date: a datetime that will be auto-generated on record creation.
    updated_date: a datetime that will be auto-generated on record creation & record updates.
    completed: a bool to mark completion of the ticket for querying.
    deleted: a bool to flag whether a record has been deleted. (we're using soft-deletion throughout the application)
    """
    id: Optional[int]
    created_date: datetime
    updated_date: datetime
    completed: bool
    deleted: bool

    def __post_init__(self):
        """
        Convert our stored dates to actual datetime implementations.

        SQLite is very limiting in how we store our data here, this ensures consistency of our data types between reads/writes.
        """
        if isinstance(self.created_date, str):
            self.created_date = datetime.strptime(self.created_date, "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.strptime(self.updated_date, "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(self.completed, int):
            self.completed = bool(self.completed)
        if isinstance(self.deleted, int):
            self.deleted = bool(self.deleted)