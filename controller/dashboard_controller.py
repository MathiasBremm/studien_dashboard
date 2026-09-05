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