from dataclasses import dataclass
from domain.studiengang import Studiengang

@dataclass
class DashboardDatenDTO:
    """DTO zur strukturierten Übergabe aller aufbereiteten UI-Daten."""

    studiengang_name: str
    ziel_durchschnitt: float
    gesamt_ects: int
    aktueller_durchschnitt: float
    notentrend: float
    trend_delta: float
    absolvierte_ects: int
    ects_soll_tempo: float
    ects_ist_tempo: float
    aktuelles_semester: int
    letztes_semester: float
    studienbeginn: date
    verstrichene_zeit_prozent: float
    semester_liste: list[Semester]