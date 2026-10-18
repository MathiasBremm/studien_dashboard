from abc import ABC, abstractmethod
from domain.studiengang import Studiengang

class IModulRepository(ABC):
    @abstractmethod
    def lade_studiengang(self) -> Studiengang:
        pass

    @abstractmethod
    def speichere_studiengang(self, studiengang: Studiengang) -> None:
        pass 
