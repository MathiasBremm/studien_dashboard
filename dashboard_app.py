from controller.dashboard_controller import DashboardController
from repository.json_modul_repository import JsonModulRepository
from service.noten_service import NotenService
from view.dashboard_view import DashboardView


class DashboardApp:
    """Application Root und Kompositionswurzel zur Instanziierung aller Kernkomponenten."""

    def start(self) -> None:
        """Initialisiert Persistenz, Services, Controller sowie View und startet den Anwendungszyklus."""
        repo = JsonModulRepository("studium_data.json")
        service = NotenService()
        controller = DashboardController(service, repo)
        view = DashboardView()

        # Daten laden und an View übergeben
        daten_dto = controller.lade_dashboard_daten()
        view.zeige_dashboard(daten_dto, controller)

if __name__ == "__main__":
    DashboardApp().start()