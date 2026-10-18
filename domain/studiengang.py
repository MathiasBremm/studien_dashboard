from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from domain.semester import Semester

@dataclass
class Studiengang:
    """Aggregat-Root für das Studien-Datenmodell zur Verwaltung von Semestern und Stammdaten."""
    
    name: str
    student_name: str
    gesamt_ects: int
    ziel_durchschnitt: float
    ziel_dauer_jahre: float
    studienbeginn: date
    semester_liste: list[Semester] = field(default_factory=list)

    def berechne_gesamt_ects(self) -> int:
        """Summiert alle bestandenen ECTS über alle Semester."""
        return sum(s.berechne_semester_ects() for s in self.semester_liste)


    def ermittle_aktuelles_semester(self) -> int:
        """Ermittelt das aktuelle Fachsemester basierend auf der Zeit seit Studienbeginn."""
        if not self.studienbeginn:
            return 1
        verstrichene_tage = (date.today() - self.studienbeginn).days
        if verstrichene_tage < 0:
            return 1
        # Ein Semester entspricht ca. einem halben Jahr (182.625 Tage)
        semester = int(verstrichene_tage / (365.25 / 2)) + 1
        return max(1, semester)

    def ermittle_letztes_geplantes_semester(self) -> int:
        """Gibt die Anzahl der Semester im Zeitraum der Zieldauer zurück (ziel_dauer_jahre * 2)."""
        return int(self.ziel_dauer_jahre * 2)