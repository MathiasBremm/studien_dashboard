from abc import ABC, abstractmethod
from domain.studiengang import Studiengang

class IModulRepository(ABC):
    """Abstrakte Schnittstelle für den Datenzugriff auf Studiengangsdaten."""
    @abstractmethod
    def lade_studiengang(self) -> Studiengang:
        """Lädt den vollständigen Objektbaum des Studiengangs aus dem persistenten Speicher.

        Returns:
            Studiengang: Das rekonstruierte Domänenmodell.
        """
        pass

    @abstractmethod
    def speichere_studiengang(self, studiengang: Studiengang) -> None:
        """Persistiert den übergebenen Studiengang-Objektbaum dauerhaft.

        Args:
            studiengang (Studiengang): Das zu speichernde Domänenobjekt.
        """
        pass 
