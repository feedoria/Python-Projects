import customtkinter as ctk

from gui.inspector import Inspector
from gui.mechanics_view import MechanicsView
from gui.tasks_view import TasksView
from gui.theme import COLORS, FONTS
from managers.project_manager import ProjectManager
from models.game_project import GameProject


class Workspace(ctk.CTkFrame):
    def __init__(
        self,
        master,
        project: GameProject,
        project_manager: ProjectManager,
        back_callback
    ):
        super().__init__(
            master,
            fg_color=COLORS["background"],
            corner_radius=0
        )

        self._project = project
        self._project_manager = project_manager
        self._back_callback = back_callback

        self._active_view = None

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=0
        )
        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=22,
            pady=22
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        self.inspector = Inspector(
            self,
            save_callback=self._save_and_refresh
        )
        self.inspector.grid(
            row=0,
            column=2,
            sticky="nsew"
        )

        self._show_overview()

    def _create_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=COLORS["sidebar"]
        )
        sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        sidebar.grid_propagate(False)

        back_button = ctk.CTkButton(
            sidebar,
            text="< Projects",
            fg_color="transparent",
            hover_color=COLORS["surface_hover"],
            anchor="w",
            command=self._back_callback
        )
        back_button.pack(
            fill="x",
            padx=15,
            pady=(18, 10)
        )

        project_name = ctk.CTkLabel(
            sidebar,
            text=self._project.name,
            font=FONTS["subtitle"],
            text_color=COLORS["text_primary"],
            wraplength=180,
            justify="left"
        )
        project_name.pack(
            anchor="w",
            padx=20,
            pady=(10, 25)
        )

        self._sidebar_button(
            sidebar,
            "Overview",
            self._show_overview
        )

        self._sidebar_button(
            sidebar,
            "Mechanics",
            self._show_mechanics
        )

        self._sidebar_button(
            sidebar,
            "Tasks",
            self._show_tasks
        )

        self._sidebar_button(
            sidebar,
            "Assets",
            lambda: self._show_placeholder("Assets")
        )

        self._sidebar_button(
            sidebar,
            "Technologies",
            lambda: self._show_placeholder(
                "Technologies"
            )
        )

    def _sidebar_button(
        self,
        parent,
        text: str,
        command
    ) -> None:
        button = ctk.CTkButton(
            parent,
            text=text,
            height=40,
            anchor="w",
            fg_color="transparent",
            hover_color=COLORS["surface_hover"],
            text_color=COLORS["text_primary"],
            command=command
        )
        button.pack(
            fill="x",
            padx=12,
            pady=3
        )

    def _clear_content(self) -> None:
        for widget in self.content.winfo_children():
            widget.destroy()

    def _create_page_header(
        self,
        title: str,
        subtitle: str
    ) -> None:
        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=FONTS["title"],
            text_color=COLORS["text_primary"]
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header,
            text=subtitle,
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        subtitle_label.pack(
            anchor="w",
            pady=(4, 0)
        )

    def _show_overview(self) -> None:
        self._clear_content()

        self._create_page_header(
            "Overview",
            "General project information and progress."
        )

        dashboard = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        dashboard.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        for column in range(3):
            dashboard.grid_columnconfigure(
                column,
                weight=1
            )

        self._stat_card(
            dashboard,
            0,
            "Progress",
            f"{self._project.calculate_progress()}%"
        )

        self._stat_card(
            dashboard,
            1,
            "Remaining Hours",
            str(
                self._project.calculate_remaining_hours()
            )
        )

        self._stat_card(
            dashboard,
            2,
            "Tasks",
            str(len(self._project.tasks))
        )

        description_card = ctk.CTkFrame(
            dashboard,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=12
        )
        description_card.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=7,
            pady=15
        )

        ctk.CTkLabel(
            description_card,
            text="Project Description",
            font=FONTS["section"],
            text_color=COLORS["text_primary"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        ctk.CTkLabel(
            description_card,
            text=self._project.description or (
                "No description added."
            ),
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        self.inspector.show_project(self._project)

    def _stat_card(
        self,
        parent,
        column: int,
        title: str,
        value: str
    ) -> None:
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=12
        )
        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=7
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 4)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=FONTS["title"],
            text_color=COLORS["accent_light"]
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 16)
        )

    def _show_mechanics(self) -> None:
        self._clear_content()

        self._create_page_header(
            "Mechanics",
            "Organize and connect the gameplay systems."
        )

        self._active_view = MechanicsView(
            self.content,
            project=self._project,
            inspector=self.inspector,
            save_callback=self._save_and_refresh
        )
        self._active_view.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.inspector.show_empty()

    def _show_tasks(self) -> None:
        self._clear_content()

        self._create_page_header(
            "Tasks",
            "Track implementation work and dependencies."
        )

        self._active_view = TasksView(
            self.content,
            project=self._project,
            inspector=self.inspector,
            save_callback=self._save_and_refresh
        )
        self._active_view.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.inspector.show_empty()

    def _show_placeholder(self, name: str) -> None:
        self._clear_content()

        self._create_page_header(
            name,
            f"The {name.lower()} view will be added next."
        )

        label = ctk.CTkLabel(
            self.content,
            text=f"{name} section",
            font=FONTS["title"],
            text_color=COLORS["text_secondary"]
        )
        label.grid(
            row=1,
            column=0
        )

        self.inspector.show_empty()

    def _save_and_refresh(self) -> None:
        self._project_manager.save()

        if self._active_view is not None:
            self._active_view.refresh()