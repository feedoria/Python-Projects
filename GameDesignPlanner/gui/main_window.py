import customtkinter as ctk

from gui.start_screen import StartScreen
from gui.workspace import Workspace
from managers.project_manager import ProjectManager
from models.game_project import GameProject


ctk.set_appearance_mode("dark")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._project_manager = ProjectManager()
        self._current_screen = None

        self.title("Game Design Planner")
        self.geometry("1400x850")
        self.minsize(1100, 700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_start_screen()

    def _clear_screen(self) -> None:
        if self._current_screen is not None:
            self._current_screen.destroy()

        self._current_screen = None

    def show_start_screen(self) -> None:
        self._clear_screen()

        self._current_screen = StartScreen(
            master=self,
            project_manager=self._project_manager,
            open_project_callback=self.open_project
        )

        self._current_screen.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def open_project(self, project: GameProject) -> None:
        self._clear_screen()

        self._current_screen = Workspace(
            master=self,
            project=project,
            project_manager=self._project_manager,
            back_callback=self.show_start_screen
        )

        self._current_screen.grid(
            row=0,
            column=0,
            sticky="nsew"
        )


def run_app() -> None:
    app = MainWindow()
    app.mainloop()