from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class ModulEintragDTO:
    semester: int
    modul_code: str
    modul_name: str
    ects: int
    status: str
    note: Optional[float] = None
    versuche: int = 1
    abgabe: Optional[date] = None
    notendatum: Optional[date] = None