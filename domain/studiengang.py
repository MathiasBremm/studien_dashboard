from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from domain.semester import Semester

@dataclass
class Studiengang:

    student_name: str
    name: str
    gesamt_ects: int
    ziel_durchschnitt: float
    ziel_dauer_jahre: float
    studienbeginn: date
    semester_liste: list[Semester] = field(default_factory=list)

    def berechne_gesamt_ects(self) -> int:
        """Summiert alle bestandenen ECTS über alle Semester."""
        return sum(s.berechne_semester_ects() for s in self.semester_liste)


    def ermittle_aktuelles_semester(self) -> int:
        """Gibt die Nummer des aktuell eingetragenen (höchsten) Semesters zurück."""
        if not self.semester_liste:
            return 1
        return max(sem.nummer for sem in self.semester_liste)

    def ermittle_letztes_geplantes_semester(self) -> float:
        """Gibt die Anzahl der Semster im Zeitraum der Zieldauer zurück. (ziel_dauer_jahre*2)"""
        return int(self.ziel_dauer_jahre * 2)