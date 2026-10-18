from typing import Optional
from domain.modul import Modul
from domain.pruefungsleistung import Pruefungsleistung
from dto.modul_eintrag_dto import ModulEintragDTO

class ModulMapper:
    """Wandelt neutrale DTO-Tabelleneinträge in Domänenobjekte um."""
    
    @staticmethod
    def dto_zu_modul(dto: ModulEintragDTO) -> Modul:
        modul = Modul(
            modul_code=dto.modul_code,
            name=dto.modul_name,
            ects=dto.ects
        )
        if dto.note is not None or dto.notendatum is not None or dto.abgabe is not None:
            pruefung = Pruefungsleistung(
                note=dto.note,
                datum=dto.notendatum,
                versuch=dto.versuche,
                abgabe=dto.abgabe
            )
            modul.fuege_pruefungsleistung_hinzu(pruefung)
        
        modul.aktualisiere_status()
        return modul