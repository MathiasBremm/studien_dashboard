from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Pruefungsleistung:

    note: Optional[float] = None
    datum: Optional[date] = None
    versuch: int = 1
    abgabe: Optional[date] = None

    def is_bestanden(self) -> bool:
        """Single Source of Truth für das Bestehen einer Prüfung."""
        return self.note is not None and self.note <= 4.0