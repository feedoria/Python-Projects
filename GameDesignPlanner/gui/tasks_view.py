import tkinter as tk

import customtkinter as ctk

from gui.theme import COLORS, FONTS
from models.enums import Priority, TaskStatus
from models.game_project import GameProject
from models.task import Task


class TasksView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        project: GameProject,
        inspector,
        save_callback
    ):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self._project = project
        self._inspector = inspector
        self._save_callback = save_callback

        self._current_mode = "Board"
        self._drag_node_id = None
        self._drag_last_x = 0
        self._drag_last_y = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_toolbar()
        self._show_board_view()

    def _create_toolbar(self) -> None:
        toolbar = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        toolbar.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        toolbar.grid_columnconfigure(1, weight=1)

        add_button = ctk.CTkButton(
            toolbar,
            text="+ Add Task",
            width=130,
            height=36,
            font=FONTS["button"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=self._open_add_dialog
        )
        add_button.grid(
            row=0,
            column=0,
            sticky="w"
        )

        dependency_button = ctk.CTkButton(
            toolbar,
            text="Add Dependency",
            width=140,
            height=36,
            fg_color=COLORS["surface"],
            hover_color=COLORS["surface_hover"],
            command=self._open_dependency_dialog
        )
        dependency_button.grid(
            row=0,
            column=1,
            sticky="w",
            padx=10
        )

        switcher = ctk.CTkSegmentedButton(
            toolbar,
            values=["Board", "Dependencies"],
            selected_color=COLORS["accent"],
            selected_hover_color=COLORS["accent_dark"],
            unselected_color=COLORS["surface"],
            unselected_hover_color=COLORS["surface_hover"],
            command=self._change_mode
        )
        switcher.grid(
            row=0,
            column=2,
            sticky="e"
        )
        switcher.set("Board")

    def _clear_content(self) -> None:
        if hasattr(self, "content"):
            self.content.destroy()

    def _change_mode(self, mode: str) -> None:
        self._current_mode = mode

        if mode == "Dependencies":
            self._show_dependency_view()
        else:
            self._show_board_view()

    def refresh(self) -> None:
        if self._current_mode == "Dependencies":
            self._show_dependency_view()
        else:
            self._show_board_view()

    def _show_board_view(self) -> None:
        self._clear_content()

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        for column in range(3):
            self.content.grid_columnconfigure(
                column,
                weight=1
            )

        self.content.grid_rowconfigure(0, weight=1)

        columns = [
            ("Not Started", TaskStatus.NOT_STARTED),
            ("In Progress", TaskStatus.IN_PROGRESS),
            ("Done", TaskStatus.DONE)
        ]

        for column_index, (
            title,
            status
        ) in enumerate(columns):
            frame = ctk.CTkScrollableFrame(
                self.content,
                label_text=title,
                label_font=FONTS["section"],
                fg_color=COLORS["sidebar"],
                border_width=1,
                border_color=COLORS["border"]
            )
            frame.grid(
                row=0,
                column=column_index,
                sticky="nsew",
                padx=6
            )

            frame.grid_columnconfigure(0, weight=1)

            tasks = [
                task
                for task in self._project.tasks
                if task.status == status
            ]

            for row, task in enumerate(tasks):
                card = ctk.CTkButton(
                    frame,
                    text=(
                        f"{task.title}\n"
                        f"{task.priority.value} | "
                        f"{task.estimated_hours} h"
                    ),
                    anchor="w",
                    height=75,
                    fg_color=COLORS["surface"],
                    hover_color=COLORS["surface_hover"],
                    command=lambda item=task: (
                        self._inspector.show_task(item)
                    )
                )
                card.grid(
                    row=row,
                    column=0,
                    sticky="ew",
                    padx=7,
                    pady=6
                )

    def _show_dependency_view(self) -> None:
        self._clear_content()

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["canvas"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self.content,
            bg=COLORS["canvas"],
            highlightthickness=0
        )
        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self._render_dependencies()

    def _render_dependencies(self) -> None:
        self.canvas.delete("all")

        positions = {}

        for index, task in enumerate(self._project.tasks):
            layout = self._project.find_layout(
                task.task_id,
                "Tasks"
            )

            if layout is None:
                x = 70 + (index % 3) * 250
                y = 70 + (index // 3) * 150

                self._project.set_node_layout(
                    task.task_id,
                    "Tasks",
                    x,
                    y
                )

                layout = self._project.find_layout(
                    task.task_id,
                    "Tasks"
                )

            positions[task.task_id] = (
                layout.position_x,
                layout.position_y,
                layout.width,
                layout.height
            )

        for dependency in self._project.task_dependencies:
            source = positions.get(
                dependency.prerequisite_task_id
            )
            target = positions.get(
                dependency.dependent_task_id
            )

            if source is None or target is None:
                continue

            self.canvas.create_line(
                source[0] + source[2],
                source[1] + source[3] / 2,
                target[0],
                target[1] + target[3] / 2,
                fill=COLORS["accent_light"],
                width=2,
                arrow=tk.LAST
            )

        for task in self._project.tasks:
            x, y, width, height = positions[task.task_id]
            tag = f"node_{task.task_id}"

            self.canvas.create_rectangle(
                x,
                y,
                x + width,
                y + height,
                fill=COLORS["surface"],
                outline=COLORS["accent_dark"],
                width=2,
                tags=(tag, "node")
            )

            self.canvas.create_text(
                x + 15,
                y + 20,
                text=task.title,
                anchor="w",
                fill=COLORS["text_primary"],
                font=FONTS["node"],
                tags=(tag, "node")
            )

            self.canvas.create_text(
                x + 15,
                y + 52,
                text=task.status.value,
                anchor="w",
                fill=COLORS["text_secondary"],
                font=FONTS["small"],
                tags=(tag, "node")
            )

            self.canvas.tag_bind(
                tag,
                "<Button-1>",
                lambda event, item=task: (
                    self._inspector.show_task(item)
                )
            )

            self.canvas.tag_bind(
                tag,
                "<ButtonPress-1>",
                lambda event, item=task: (
                    self._start_drag(
                        event,
                        item.task_id
                    )
                )
            )

            self.canvas.tag_bind(
                tag,
                "<B1-Motion>",
                self._drag_node
            )

            self.canvas.tag_bind(
                tag,
                "<ButtonRelease-1>",
                self._finish_drag
            )

    def _start_drag(
        self,
        event,
        task_id: str
    ) -> None:
        self._drag_node_id = task_id
        self._drag_last_x = event.x
        self._drag_last_y = event.y

    def _drag_node(self, event) -> None:
        if self._drag_node_id is None:
            return

        dx = event.x - self._drag_last_x
        dy = event.y - self._drag_last_y

        self.canvas.move(
            f"node_{self._drag_node_id}",
            dx,
            dy
        )

        self._drag_last_x = event.x
        self._drag_last_y = event.y

    def _finish_drag(self, event) -> None:
        if self._drag_node_id is None:
            return

        bbox = self.canvas.bbox(
            f"node_{self._drag_node_id}"
        )

        if bbox is not None:
            self._project.set_node_layout(
                self._drag_node_id,
                "Tasks",
                bbox[0],
                bbox[1]
            )

            self._save_callback()

        self._drag_node_id = None
        self._render_dependencies()

    def _open_add_dialog(self) -> None:
        dialog = ctk.CTkToplevel(self)

        dialog.title("Add Task")
        dialog.geometry("500x620")
        dialog.configure(fg_color=COLORS["background"])
        dialog.grab_set()

        frame = ctk.CTkScrollableFrame(
            dialog,
            fg_color=COLORS["surface"]
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        title = self._dialog_entry(frame, "Title")

        status = self._dialog_option(
            frame,
            "Status",
            [item.value for item in TaskStatus],
            TaskStatus.NOT_STARTED.value
        )

        priority = self._dialog_option(
            frame,
            "Priority",
            [item.value for item in Priority],
            Priority.MEDIUM.value
        )

        difficulty = self._dialog_entry(
            frame,
            "Difficulty",
            "1"
        )

        hours = self._dialog_entry(
            frame,
            "Estimated hours",
            "0"
        )

        ctk.CTkLabel(
            frame,
            text="Description",
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        description = ctk.CTkTextbox(
            frame,
            height=110
        )
        description.pack(
            fill="x",
            padx=20
        )

        error = ctk.CTkLabel(
            frame,
            text="",
            text_color=COLORS["danger"]
        )
        error.pack(pady=5)

        def add() -> None:
            try:
                task = Task(
                    title=title.get(),
                    description=description.get(
                        "1.0",
                        "end"
                    ).strip(),
                    status=TaskStatus(status.get()),
                    priority=Priority(priority.get()),
                    difficulty=int(difficulty.get()),
                    estimated_hours=float(hours.get())
                )

                self._project.add_task(task)
                self._save_callback()

                dialog.destroy()
                self.refresh()

            except (ValueError, TypeError) as exception:
                error.configure(text=str(exception))

        ctk.CTkButton(
            frame,
            text="Add Task",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=add
        ).pack(
            fill="x",
            padx=20,
            pady=15
        )

    def _open_dependency_dialog(self) -> None:
        tasks = self._project.tasks

        if len(tasks) < 2:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Task Dependency")
        dialog.geometry("450x350")
        dialog.configure(fg_color=COLORS["background"])
        dialog.grab_set()

        frame = ctk.CTkFrame(
            dialog,
            fg_color=COLORS["surface"]
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        names = [task.title for task in tasks]

        prerequisite = self._dialog_option(
            frame,
            "Prerequisite task",
            names,
            names[0]
        )

        dependent = self._dialog_option(
            frame,
            "Dependent task",
            names,
            names[1]
        )

        error = ctk.CTkLabel(
            frame,
            text="",
            text_color=COLORS["danger"]
        )
        error.pack(pady=10)

        def add_dependency() -> None:
            try:
                prerequisite_task = next(
                    task
                    for task in tasks
                    if task.title == prerequisite.get()
                )

                dependent_task = next(
                    task
                    for task in tasks
                    if task.title == dependent.get()
                )

                self._project.add_task_dependency(
                    prerequisite_task.task_id,
                    dependent_task.task_id
                )

                self._save_callback()
                dialog.destroy()
                self.refresh()

            except (ValueError, TypeError) as exception:
                error.configure(text=str(exception))

        ctk.CTkButton(
            frame,
            text="Add Dependency",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=add_dependency
        ).pack(
            fill="x",
            padx=20,
            pady=15
        )

    @staticmethod
    def _dialog_entry(
        parent,
        label: str,
        default: str = ""
    ):
        ctk.CTkLabel(
            parent,
            text=label,
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        entry = ctk.CTkEntry(parent)
        entry.pack(
            fill="x",
            padx=20
        )

        if default:
            entry.insert(0, default)

        return entry

    @staticmethod
    def _dialog_option(
        parent,
        label: str,
        values: list[str],
        default: str
    ):
        ctk.CTkLabel(
            parent,
            text=label,
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        option = ctk.CTkOptionMenu(
            parent,
            values=values
        )
        option.pack(
            fill="x",
            padx=20
        )
        option.set(default)

        return option