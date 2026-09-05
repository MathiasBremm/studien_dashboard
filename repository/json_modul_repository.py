import json
from datetime import datetime, date
from pathlib import Path

from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsleistung import Pruefungsleistung
from domain.semester import Semester
from domain.studiengang import Studiengang

class JsonModulRepository:
    """Repository zum Laden und Speichern des Studienzustands via JSON."""

    def __init__(self, dateipfad: str = "studium_data.json"):
        self.dateipfad = Path(dateipfad)

    def lade_studiengang(self) -> Studiengang:
        """Lädt den vollständigen Objektbaum aus der JSON-Datei."""
        if not self.dateipfad.exists():
            return Studiengang(name="Nicht definiert")

        with open(self.dateipfad, "r", encoding="utf-8") as f:
            data = json.load(f)

        studiengang = Studiengang(
            name=data.get("studiengang", "Nicht definiert"),
            gesamt_ects=data.get("gesamt_ects", 0),
            ziel_durchschnitt=data.get("ziel_durchschnitt", 0.0),
            ziel_dauer_jahre=data.get("ziel_dauer_jahre", 0.0),
            studienbeginn=date.fromisoformat(data.get("studienbeginn", "2099-01-01"))
        )

        for sem_data in data.get("semester_liste", []):
            semester = Semester(
                nummer=sem_data["nummer"], bezeichnung=sem_data["bezeichnung"]
            )
            for mod_data in sem_data.get("module", []):
                modul = Modul(
                    modul_code=mod_data["modul_code"],
                    name=mod_data["name"],
                    ects=mod_data["ects"],
                    status=ModulStatus[mod_data["status"]],
                )
                for p_data in mod_data.get("pruefungsleistungen", []):
                    datum_val = (
                        datetime.strptime(p_data["datum"], "%Y-%m-%d").date()
                        if p_data.get("datum")
                        else None
                    )
                    pruefung = Pruefungsleistung(
                        note=p_data.get("note"),
                        datum=datum_val,
                        versuch=p_data.get("versuch", 1),
                    )
                    modul.fuege_pruefungsleistung_hinzu(pruefung)
                semester.module.append(modul)
            studiengang.semester_liste.append(semester)

        return studiengang