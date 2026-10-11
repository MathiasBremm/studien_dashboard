from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.semester import Semester

@dataclass
class DashboardDatenDTO:
    """DTO zur strukturierten Übergabe der Semesterdaten"""

    student_name: str
    studiengang_name: str
    ziel_durchschnitt: float
    gesamt_ects: int
    aktueller_durchschnitt: float
    notentrend: float
    trend_delta: Optional[float]
    absolvierte_ects: int
    ects_soll_tempo: float
    ects_ist_tempo: float
    aktuelles_semester: int
    letztes_semester: int
    studienbeginn: date
    verstrichene_zeit_prozent: float
    semester_liste: list[Semester]