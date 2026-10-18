from __future__ import annotations
from dataclasses import dataclass, field
from domain.modul_status import ModulStatus
from domain.pruefungsleistung import Pruefungsleistung

@dataclass
class Modul:
    """Repräsentiert ein Studienmodul inklusive zugehöriger Prüfungsleistungen und Bearbeitungsstatus."""

    modul_code: str
    name: str
    ects: int
    status: ModulStatus = ModulStatus.OFFEN
    pruefungsleistungen: list[Pruefungsleistung] = field(default_factory=list)

    def fuege_pruefungsleistung_hinzu(self, pruefung: Pruefungsleistung) -> None:
        """Fügt dem Modul eine Prüfungsleistung hinzu."""
        self.pruefungsleistungen.append(pruefung)

    def aktualisiere_status(self) -> ModulStatus:
        """Ermittelt und aktualisiert den Modulstatus anhand der Prüfungsleistungen."""
        if not self.pruefungsleistungen:
            return self.status

        letzte_leistung = self.pruefungsleistungen[-1]
        if letzte_leistung.note is not None:
            self.status = ModulStatus.BESTANDEN if letzte_leistung.note <= 4.0 else ModulStatus.NICHT_BESTANDEN
        elif letzte_leistung.abgabe is not None:
            self.status = ModulStatus.WARTE_AUF_NOTE
        elif letzte_leistung.datum is not None:
            self.status = ModulStatus.IN_BEARBEITUNG
        return self.status