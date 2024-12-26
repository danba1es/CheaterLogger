from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Cheater:
    id: int
    gamertag: str
    reporter_id: int
    timestamp: datetime
    is_banned: bool
    map_location: Optional[str] = None
    base_location: Optional[str] = None
    spi_command: Optional[str] = None
