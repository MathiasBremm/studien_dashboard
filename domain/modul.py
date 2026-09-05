from __future__ import annotations
from dataclasses import dataclass, field
from domain.modul_status import ModulStatus
from domain.pruefungsleistung import Pruefungsleistung

@dataclass
class Modul:

    modul_code: str
    name: str
    ects: int
    status: ModulStatus = ModulStatus.OFFEN
    pruefungsleistungen: list[Pruefungsleistung] = field(default_factory=list)

    def fuege_pruefungsleistung_hinzu(self, pruefung: Pruefungsleistung) -> None:
        """Fügt dem Modul eine Prüfungsleistung hinzu."""
        self.pruefungsleistungen.append(pruefung)