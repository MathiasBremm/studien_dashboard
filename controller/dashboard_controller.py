from __future__ import annotations
from datetime import date, datetime
from typing import Optional
import pandas as pd

from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from dto.dashboard_daten_dto import DashboardDatenDTO
from repository.json_modul_repository import JsonModulRepository
from service.noten_service import NotenService

class DashboardController:
    """Controller zur Orchestrierung zwischen UI, Logik und Datenhaltung."""

    def __init__(
        self, noten_service: NotenService, repository: JsonModulRepository
    ):
        self.noten_service = noten_service
        self.repository = repository

    def lade_dashboard_daten(self) -> DashboardDatenDTO:
        """Bereitet alle Daten auf und übergibt sie strukturiert als DTO."""

        studiengang = self.repository.lade_studiengang()
        aktuelles_sem = studiengang.ermittle_aktuelles_semester()
        letztes_sem = studiengang.ermittle_letztes_geplantes_semester()
        durchschnitt = self.noten_service.berechne_gesamtschnitt(studiengang)
        notentrend, trend_delta = self.noten_service.berechne_notentrend(studiengang)
        absolvierte_ects = studiengang.berechne_gesamt_ects()
        soll_tempo = self.noten_service.berechne_ects_soll_tempo(studiengang)
        ist_tempo = self.noten_service.berechne_ects_ist_tempo(studiengang, aktuelles_sem)
        studienbeginn = studiengang.studienbeginn
        verstrichene_zeit_prozent = self.noten_service.berechne_verstrichene_zeit_prozent(studiengang)
        semester_liste = studiengang.semester_liste

        return DashboardDatenDTO(

            student_name=studiengang.student_name,
            studiengang_name=studiengang.name,
            ziel_durchschnitt=studiengang.ziel_durchschnitt,
            gesamt_ects=studiengang.gesamt_ects,
            aktueller_durchschnitt=durchschnitt,
            notentrend=notentrend,
            trend_delta=trend_delta,
            absolvierte_ects=absolvierte_ects,
            ects_soll_tempo=soll_tempo,
            ects_ist_tempo=ist_tempo,
            aktuelles_semester=aktuelles_sem,
            letztes_semester=letztes_sem,
            studienbeginn=studiengang.studienbeginn,
            verstrichene_zeit_prozent=verstrichene_zeit_prozent,
            semester_liste=studiengang.semester_liste,
        )

    def speichere_dashboard_daten(self, daten_df: pd.DataFrame) -> None:
        """Nimmt die editierten Tabellendaten aus der View und übergibt sie an das Repository zum speichern"""
        studiengang = self.repository.lade_studiengang()

        semester_dict: dict[int, Semester] = {}

        for _, row in daten_df.iterrows():
            if pd.isna(row.get("Modulcode")) or pd.isna(row.get("Semester")):
                continue

            sem_nr = int(row["Semester"])
            if sem_nr not in semester_dict:
                semester_dict[sem_nr] = Semester(
                    nummer=sem_nr,
                    bezeichnung=f"{sem_nr}. Semester",
                )

            # Prüfungsdaten extrahieren
            note_raw = row.get("Note")
            note_val = float(note_raw) if pd.notna(note_raw) and note_raw is not None else None

            versuch_raw = row.get("Versuche")
            versuch_val = int(versuch_raw) if pd.notna(versuch_raw) and versuch_raw is not None else 1

            notendatum_val = self._zu_datum(row.get("Notendatum"))
            abgabe_val = self._zu_datum(row.get("Abgabe"))

            pruefung = Pruefungsleistung(
                note=note_val,
                datum=notendatum_val,
                versuch=versuch_val,
                abgabe=abgabe_val,
            )

            modul = Modul(
                modul_code=str(row.get("Modulcode", "")),
                name=str(row.get("Modulname", "")),
                ects=int(row.get("ECTS", 5)),
            )

            # Prüfungsleistung anhängen, wenn relevante Angaben vorliegen
            if note_val is not None or notendatum_val is not None or abgabe_val is not None:
                modul.fuege_pruefungsleistung_hinzu(pruefung)

            # Fachlogik: Modulstatus aus Prüfungsleistung ermitteln
            modul.aktualisiere_status()

            semester_dict[sem_nr].module.append(modul)

        # Semester sortieren, im Modell aktualisieren und speichern
        studiengang.semester_liste = sorted(semester_dict.values(), key=lambda s: s.nummer)
        self.repository.speichere_studiengang(studiengang)

    @staticmethod
    def _zu_datum(wert) -> Optional[date]:
        """Hilfsmethode: Konvertiert Eingabedaten sicher in ein date-Objekt."""
        if pd.isna(wert) or wert is None:
            return None
        if isinstance(wert, (datetime, pd.Timestamp)):
            return wert.date()
        if isinstance(wert, date):
            return wert
        if isinstance(wert, str) and wert.strip():
            try:
                return datetime.strptime(wert.strip(), "%Y-%m-%d").date()
            except ValueError:
                return None
        return None