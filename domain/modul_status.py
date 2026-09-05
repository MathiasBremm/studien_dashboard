from enum import Enum

class ModulStatus(Enum):
    """Aufzählungstyp für den Bearbeitungsstatus eines Moduls."""

    OFFEN = "OFFEN"
    IN_BEARBEITUNG = "IN_BEARBEITUNG"
    WARTE_AUF_NOTE = "WARTE_AUF_NOTE"
    BESTANDEN = "BESTANDEN"