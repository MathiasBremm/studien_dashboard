from controller.dashboard_controller import DashboardController
from repository.json_modul_repository import JsonModulRepository
from service.noten_service import NotenService
from view.dashboard_view import DashboardView


class DashboardApp:

    def start(self) -> None:
        repo = JsonModulRepository("studium_data.json")
        service = NotenService()
        controller = DashboardController(service, repo)
        view = DashboardView()

        # Daten laden und an View übergeben
        daten_dto = controller.lade_dashboard_daten()
        view.zeige_dashboard(daten_dto)

if __name__ == "__main__":
    DashboardApp().start()