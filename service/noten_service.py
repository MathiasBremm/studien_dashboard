from __future__ import annotations
from datetime import date
from typing import Optional
from domain.studiengang import Studiengang

class NotenService:
    """Service-Klasse für Berechnungen und Auswertungen."""

    def berechne_gesamtschnitt(self, studiengang: Studiengang) -> float:
        """Berechnet den gewichteten Notendurchschnitt über alle bestandenen Module."""

        gesamt_gewichtete_note = 0.0
        gesamt_ects = 0

        for semester in studiengang.semester_liste:
            for modul in semester.module:
                # Letzte bestandene Prüfungsleistung heranziehen
                bestandene = [
                    p for p in modul.pruefungsleistungen if p.is_bestanden()
                ]
                if bestandene and bestandene[-1].note is not None:
                    gesamt_gewichtete_note += bestandene[-1].note * modul.ects
                    gesamt_ects += modul.ects

        if gesamt_ects == 0:
            return 0.0
        return round(gesamt_gewichtete_note / gesamt_ects, 2)

    def berechne_notentrend(
        self, studiengang: Studiengang, anzahl: int = 3
    ) -> tuple[float, Optional[float]]:
        """Berechnet den Durchschnitt der letzten N absolvierten Prüfungen und die Differenz zur vorherigen Periode."""

        alle_pruefungen = []
        for semester in studiengang.semester_liste:
            for modul in semester.module:
                for p in modul.pruefungsleistungen:
                    if p.note is not None:
                        alle_pruefungen.append(p)

        if not alle_pruefungen:
            return 0.0, None

        # Sortierung nach Datum (falls kein Datum hinterlegt ist, date.min als Fallback)
        alle_pruefungen.sort(key=lambda p: p.datum or date.min)

        noten = [p.note for p in alle_pruefungen]

        if len(noten) < anzahl:
            aktueller_schnitt = (
                round(sum(noten) / len(noten), 2)
            )
            return aktueller_schnitt, None

        aktueller_trend = round(sum(noten[-anzahl:]) / anzahl, 2)

        if len(noten) >= (anzahl+1):
            vorheriger_trend = round(sum(noten[-(anzahl+1):-1]) / anzahl, 2)
            delta = round(vorheriger_trend - aktueller_trend, 2)
        else:
            delta = None

        return aktueller_trend, delta

    def berechne_ects_soll_tempo(self, studiengang: Studiengang) -> float:
        """Berechnet das Ziel-Tempo in ECTS pro Semester."""

        anzahl_semester = studiengang.ziel_dauer_jahre * 2
        if anzahl_semester == 0:
            return 0.0
        return round(studiengang.gesamt_ects / anzahl_semester, 1)

    def berechne_ects_ist_tempo(
        self, studiengang: Studiengang, aktuelles_semester: int
    ) -> float:
        """Berechnet das bisherige Durchschnittstempo in ECTS pro Semester."""

        if aktuelles_semester <= 0:
            return 0.0
        absolvierte_ects = studiengang.berechne_gesamt_ects()
        return round(absolvierte_ects / aktuelles_semester, 1)

    def berechne_verstrichene_zeit_prozent(
        self, studiengang: Studiengang) -> float:
        """Berechnet den Prozentsatz der verstrichenen Zeit im Verhältnis zur geplanten Studiendauer."""        

        if not studiengang.studienbeginn or studiengang.ziel_dauer_jahre <= 0:
            return 0.0

        aktuelles_datum = date.today()

        # Die Dauer muss mit 365.25 gerechnet werden, wegen den Schaltjahren
        gesamtdauer_tage = studiengang.ziel_dauer_jahre * 365.25
        verstrichene_tage = (aktuelles_datum - studiengang.studienbeginn).days

        if verstrichene_tage <= 0:
            return 0.0

        prozent = (verstrichene_tage / gesamtdauer_tage) * 100.0
        return min(round(prozent, 1), 100.0)