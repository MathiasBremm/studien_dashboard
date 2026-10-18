
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from dto.dashboard_daten_dto import DashboardDatenDTO
from repository.i_modul_repository import IModulRepository
from service.noten_service import NotenService
from dto.modul_eintrag_dto import ModulEintragDTO
from mapper.modul_mapper import ModulMapper

class DashboardController:
    """Controller zur Orchestrierung zwischen UI, Logik und Datenhaltung."""

    def __init__(
        self, noten_service: NotenService, repository: IModulRepository
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

    def speichere_dashboard_daten(self, eintraege: list[ModulEintragDTO]) -> None:
        studiengang = self.repository.lade_studiengang()
        semester_dict: dict[int, Semester] = {}

        for zeile in eintraege:
            if not zeile.modul_code or zeile.semester <= 0:
                continue

            if zeile.semester not in semester_dict:
                semester_dict[zeile.semester] = Semester(
                    nummer=zeile.semester,
                    bezeichnung=f"{zeile.semester}. Semester"
                )

            modul = ModulMapper.dto_zu_modul(zeile)
            semester_dict[zeile.semester].module.append(modul)

        studiengang.semester_liste = sorted(semester_dict.values(), key=lambda s: s.nummer)
        self.repository.speichere_studiengang(studiengang)