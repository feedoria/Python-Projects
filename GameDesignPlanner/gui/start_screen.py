import customtkinter as ctk

from gui.theme import COLORS, FONTS
from managers.project_manager import ProjectManager
from models.enums import ProjectStatus
from models.game_project import GameProject


class StartScreen(ctk.CTkFrame):
    def __init__(
        self,
        master,
        project_manager: ProjectManager,
        open_project_callback
    ):
        super().__init__(
            master,
            fg_color=COLORS["background"],
            corner_radius=0
        )

        self._project_manager = project_manager
        self._open_project_callback = open_project_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_interface()

    def _create_interface(self) -> None:
        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=55,
            pady=45
        )

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        self._create_header(container)
        self._create_separator(container)
        self._create_projects_section(container)

    def _create_header(self, parent) -> None:
        header = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Game Design Planner",
            font=FONTS["app_title"],
            text_color=COLORS["text_primary"]
        )
        title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Turn your game idea into a clear development plan.",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"]
        )
        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(6, 0)
        )

        new_button = ctk.CTkButton(
            header,
            text="+ New Project",
            width=160,
            height=42,
            corner_radius=10,
            font=FONTS["button"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=self._open_new_project_dialog
        )
        new_button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(20, 0)
        )

    def _create_separator(self, parent) -> None:
        separator = ctk.CTkFrame(
            parent,
            height=1,
            fg_color=COLORS["border"]
        )
        separator.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=30
        )

    def _create_projects_section(self, parent) -> None:
        section = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        section.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        section.grid_columnconfigure(0, weight=1)
        section.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            section,
            text="Recent Projects",
            font=FONTS["subtitle"],
            text_color=COLORS["text_primary"]
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 15)
        )

        self.projects_frame = ctk.CTkScrollableFrame(
            section,
            fg_color=COLORS["sidebar"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.projects_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.projects_frame.grid_columnconfigure(0, weight=1)

        self._display_projects()

    def _display_projects(self) -> None:
        for widget in self.projects_frame.winfo_children():
            widget.destroy()

        projects = self._project_manager.projects

        if not projects:
            empty_label = ctk.CTkLabel(
                self.projects_frame,
                text="No projects yet.\nCreate your first game project.",
                font=FONTS["body"],
                text_color=COLORS["text_secondary"],
                justify="center"
            )
            empty_label.grid(
                row=0,
                column=0,
                pady=70
            )
            return

        for index, project in enumerate(projects):
            self._create_project_card(project, index)

    def _create_project_card(
        self,
        project: GameProject,
        row: int
    ) -> None:
        card = ctk.CTkFrame(
            self.projects_frame,
            fg_color=COLORS["surface"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        card.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=12,
            pady=8
        )

        card.grid_columnconfigure(0, weight=1)

        name_label = ctk.CTkLabel(
            card,
            text=project.name,
            font=FONTS["subtitle"],
            text_color=COLORS["text_primary"]
        )
        name_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(15, 4)
        )

        details = ctk.CTkLabel(
            card,
            text=(
                f"{project.genre}   |   "
                f"{project.platform}   |   "
                f"{project.status.value}"
            ),
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        )
        details.grid(
            row=1,
            column=0,
            sticky="w",
            padx=18
        )

        progress = ctk.CTkLabel(
            card,
            text=f"{project.calculate_progress()}% complete",
            font=FONTS["small"],
            text_color=COLORS["accent_light"]
        )
        progress.grid(
            row=2,
            column=0,
            sticky="w",
            padx=18,
            pady=(5, 15)
        )

        open_button = ctk.CTkButton(
            card,
            text="Open",
            width=100,
            height=34,
            corner_radius=8,
            fg_color=COLORS["accent_dark"],
            hover_color=COLORS["accent"],
            command=lambda: self._open_project_callback(project)
        )
        open_button.grid(
            row=0,
            column=1,
            rowspan=3,
            padx=18
        )

    def _open_new_project_dialog(self) -> None:
        dialog = ctk.CTkToplevel(self)

        dialog.title("New Project")
        dialog.geometry("540x750")
        dialog.minsize(540, 700)       
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS["background"])
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        form = ctk.CTkScrollableFrame(
        dialog,
        fg_color=COLORS["surface"],
        corner_radius=14
        )
        form.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        title = ctk.CTkLabel(
            form,
            text="Create New Project",
            font=FONTS["title"],
            text_color=COLORS["text_primary"]
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        name_entry = self._create_entry(
            form,
            "Project name"
        )

        genre_entry = self._create_entry(
            form,
            "Genre"
        )

        platform_entry = self._create_entry(
            form,
            "Platform",
            "PC"
        )

        difficulty_entry = self._create_entry(
            form,
            "Difficulty (1-10)",
            "1"
        )

        ctk.CTkLabel(
            form,
            text="Description",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(10, 5)
        )

        description_box = ctk.CTkTextbox(
            form,
            height=100,
            fg_color=COLORS["surface_light"],
            border_width=1,
            border_color=COLORS["border"]
        )
        description_box.pack(
            fill="x",
            padx=25
        )

        error_label = ctk.CTkLabel(
            form,
            text="",
            font=FONTS["small"],
            text_color=COLORS["danger"]
        )
        error_label.pack(
            pady=(10, 0)
        )

        def create_project() -> None:
            try:
                difficulty = int(difficulty_entry.get())

                project = GameProject(
                    name=name_entry.get(),
                    genre=genre_entry.get(),
                    description=description_box.get(
                        "1.0",
                        "end"
                    ).strip(),
                    platform=platform_entry.get(),
                    status=ProjectStatus.IDEA,
                    difficulty=difficulty
                )

                self._project_manager.add_project(project)

                dialog.destroy()
                self._open_project_callback(project)

            except (ValueError, TypeError) as error:
                error_label.configure(text=str(error))

        create_button = ctk.CTkButton(
            form,
            text="Create Project",
            height=42,
            font=FONTS["button"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=create_project
        )
        create_button.pack(
            fill="x",
            padx=25,
            pady=20
        )

    @staticmethod
    def _create_entry(
        parent,
        label_text: str,
        default_value: str = ""
    ):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=25,
            pady=(8, 5)
        )

        entry = ctk.CTkEntry(
            parent,
            height=38,
            fg_color=COLORS["surface_light"],
            border_color=COLORS["border"]
        )
        entry.pack(
            fill="x",
            padx=25
        )

        if default_value:
            entry.insert(0, default_value)

        return entry