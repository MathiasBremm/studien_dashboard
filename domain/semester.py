from __future__ import annotations
from dataclasses import dataclass, field
from domain.modul import Modul


@dataclass
class Semester:
    """Verwaltet einen Studienabschnitt und aggregiert die darin enthaltenen Module."""

    nummer: int
    bezeichnung: str
    module: list[Modul] = field(default_factory=list)

    def berechne_semester_ects(self) -> int:
        """Berechnet die gewerteten ECTS-Punkte des Semesters."""
        return sum(
            m.ects
            for m in self.module
            if any(p.is_bestanden() for p in m.pruefungsleistungen)
        )