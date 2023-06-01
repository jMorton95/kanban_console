from dataclasses import dataclass
from typing import Optional

@dataclass
class TicketPreviewModel():
    id: Optional[int]
    priority: int
    title: str
    remaining_time: float
    