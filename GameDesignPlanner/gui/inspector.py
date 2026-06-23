import customtkinter as ctk

from gui.theme import COLORS, FONTS
from models.enums import Priority, ProjectStatus, TaskStatus
from models.game_project import GameProject
from models.mechanic import Mechanic
from models.task import Task


class Inspector(ctk.CTkFrame):
    def __init__(
        self,
        master,
        save_callback
    ):
        super().__init__(
            master,
            fg_color=COLORS["sidebar"],
            corner_radius=0,
            width=330
        )

        self._save_callback = save_callback
        self._selected_object = None

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="INSPECTOR",
            font=FONTS["section"],
            text_color=COLORS["accent_light"]
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        self.show_empty()

    def _clear(self) -> None:
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_empty(self) -> None:
        self._clear()
        self._selected_object = None

        label = ctk.CTkLabel(
            self.content,
            text=(
                "Select a project element\n"
                "to view and edit its details."
            ),
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            justify="center"
        )
        label.pack(
            pady=80
        )

    def show_project(self, project: GameProject) -> None:
        self._clear()
        self._selected_object = project

        self._create_heading("Project")

        name = self._entry("Name", project.name)
        genre = self._entry("Genre", project.genre)
        platform = self._entry("Platform", project.platform)

        difficulty = self._entry(
            "Difficulty",
            str(project.difficulty)
        )

        status = self._option(
            "Status",
            [item.value for item in ProjectStatus],
            project.status.value
        )

        description = self._textbox(
            "Description",
            project.description
        )

        def save() -> None:
            try:
                project.name = name.get()
                project.genre = genre.get()
                project.platform = platform.get()
                project.difficulty = int(difficulty.get())
                project.status = ProjectStatus(status.get())
                project.description = description.get(
                    "1.0",
                    "end"
                ).strip()

                self._show_success("Project saved.")
                self._save_callback()

            except (ValueError, TypeError) as error:
                self._show_error(str(error))

        self._save_button(save)

    def show_mechanic(self, mechanic: Mechanic) -> None:
        self._clear()
        self._selected_object = mechanic

        self._create_heading("Mechanic")

        name = self._entry("Name", mechanic.name)

        priority = self._option(
            "Priority",
            [item.value for item in Priority],
            mechanic.priority.value
        )

        description = self._textbox(
            "Description",
            mechanic.description
        )

        def save() -> None:
            try:
                mechanic.name = name.get()
                mechanic.priority = Priority(priority.get())
                mechanic.description = description.get(
                    "1.0",
                    "end"
                ).strip()

                self._show_success("Mechanic saved.")
                self._save_callback()

            except (ValueError, TypeError) as error:
                self._show_error(str(error))

        self._save_button(save)

    def show_task(self, task: Task) -> None:
        self._clear()
        self._selected_object = task

        self._create_heading("Task")

        title = self._entry("Title", task.title)

        status = self._option(
            "Status",
            [item.value for item in TaskStatus],
            task.status.value
        )

        priority = self._option(
            "Priority",
            [item.value for item in Priority],
            task.priority.value
        )

        difficulty = self._entry(
            "Difficulty",
            str(task.difficulty)
        )

        estimated_hours = self._entry(
            "Estimated hours",
            str(task.estimated_hours)
        )

        description = self._textbox(
            "Description",
            task.description
        )

        def save() -> None:
            try:
                task.title = title.get()
                task.status = TaskStatus(status.get())
                task.priority = Priority(priority.get())
                task.difficulty = int(difficulty.get())
                task.estimated_hours = float(
                    estimated_hours.get()
                )
                task.description = description.get(
                    "1.0",
                    "end"
                ).strip()

                self._show_success("Task saved.")
                self._save_callback()

            except (ValueError, TypeError) as error:
                self._show_error(str(error))

        self._save_button(save)

    def _create_heading(self, text: str) -> None:
        label = ctk.CTkLabel(
            self.content,
            text=text,
            font=FONTS["subtitle"],
            text_color=COLORS["text_primary"]
        )
        label.pack(
            anchor="w",
            padx=10,
            pady=(10, 18)
        )

    def _entry(
        self,
        label_text: str,
        value: str
    ):
        self._field_label(label_text)

        entry = ctk.CTkEntry(
            self.content,
            height=36,
            fg_color=COLORS["surface"],
            border_color=COLORS["border"]
        )
        entry.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
        entry.insert(0, value)

        return entry

    def _option(
        self,
        label_text: str,
        values: list[str],
        selected: str
    ):
        self._field_label(label_text)

        option = ctk.CTkOptionMenu(
            self.content,
            values=values,
            fg_color=COLORS["surface"],
            button_color=COLORS["accent_dark"],
            button_hover_color=COLORS["accent"]
        )
        option.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
        option.set(selected)

        return option

    def _textbox(
        self,
        label_text: str,
        value: str
    ):
        self._field_label(label_text)

        textbox = ctk.CTkTextbox(
            self.content,
            height=130,
            fg_color=COLORS["surface"],
            border_width=1,
            border_color=COLORS["border"]
        )
        textbox.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
        textbox.insert("1.0", value)

        return textbox

    def _field_label(self, text: str) -> None:
        label = ctk.CTkLabel(
            self.content,
            text=text,
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        )
        label.pack(
            anchor="w",
            padx=10,
            pady=(3, 4)
        )

    def _save_button(self, command) -> None:
        button = ctk.CTkButton(
            self.content,
            text="Save Changes",
            height=40,
            font=FONTS["button"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=command
        )
        button.pack(
            fill="x",
            padx=10,
            pady=(15, 10)
        )

        self.message_label = ctk.CTkLabel(
            self.content,
            text="",
            font=FONTS["small"]
        )
        self.message_label.pack(
            pady=(0, 15)
        )

    def _show_success(self, message: str) -> None:
        self.message_label.configure(
            text=message,
            text_color=COLORS["success"]
        )

    def _show_error(self, message: str) -> None:
        self.message_label.configure(
            text=message,
            text_color=COLORS["danger"]
        )