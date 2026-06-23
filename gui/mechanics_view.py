import tkinter as tk

import customtkinter as ctk

from gui.theme import COLORS, FONTS
from models.enums import Priority
from models.game_project import GameProject
from models.mechanic import Mechanic


class MechanicsView(ctk.CTkFrame):
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

        self._current_mode = "List"
        self._drag_node_id = None
        self._drag_last_x = 0
        self._drag_last_y = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_toolbar()
        self._show_list_view()

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
            text="+ Add Mechanic",
            width=145,
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

        connect_button = ctk.CTkButton(
            toolbar,
            text="Connect",
            width=100,
            height=36,
            fg_color=COLORS["surface"],
            hover_color=COLORS["surface_hover"],
            command=self._open_connect_dialog
        )
        connect_button.grid(
            row=0,
            column=1,
            sticky="w",
            padx=10
        )

        switcher = ctk.CTkSegmentedButton(
            toolbar,
            values=["List", "Flow"],
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
        switcher.set("List")

    def _clear_content(self) -> None:
        if hasattr(self, "content"):
            self.content.destroy()

    def _change_mode(self, mode: str) -> None:
        self._current_mode = mode

        if mode == "Flow":
            self._show_flow_view()
        else:
            self._show_list_view()

    def refresh(self) -> None:
        if self._current_mode == "Flow":
            self._show_flow_view()
        else:
            self._show_list_view()

    def _show_list_view(self) -> None:
        self._clear_content()

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["sidebar"],
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

        if not self._project.mechanics:
            label = ctk.CTkLabel(
                self.content,
                text="No mechanics added yet.",
                font=FONTS["body"],
                text_color=COLORS["text_secondary"]
            )
            label.grid(
                row=0,
                column=0,
                pady=60
            )
            return

        for index, mechanic in enumerate(
            self._project.mechanics
        ):
            card = ctk.CTkButton(
                self.content,
                text=(
                    f"{mechanic.name}\n"
                    f"Priority: {mechanic.priority.value}"
                ),
                anchor="w",
                height=75,
                corner_radius=10,
                fg_color=COLORS["surface"],
                hover_color=COLORS["surface_hover"],
                text_color=COLORS["text_primary"],
                font=FONTS["body"],
                command=lambda item=mechanic: (
                    self._inspector.show_mechanic(item)
                )
            )
            card.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=12,
                pady=7
            )

    def _show_flow_view(self) -> None:
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

        self._render_flow()

    def _render_flow(self) -> None:
        self.canvas.delete("all")

        positions = {}

        for index, mechanic in enumerate(
            self._project.mechanics
        ):
            layout = self._project.find_layout(
                mechanic.mechanic_id,
                "Mechanics"
            )

            if layout is None:
                x = 70 + (index % 3) * 250
                y = 70 + (index // 3) * 150

                self._project.set_node_layout(
                    mechanic.mechanic_id,
                    "Mechanics",
                    x,
                    y
                )

                layout = self._project.find_layout(
                    mechanic.mechanic_id,
                    "Mechanics"
                )

            positions[mechanic.mechanic_id] = (
                layout.position_x,
                layout.position_y,
                layout.width,
                layout.height
            )

        for connection in self._project.mechanic_connections:
            source = positions.get(
                connection.source_mechanic_id
            )
            target = positions.get(
                connection.target_mechanic_id
            )

            if source is None or target is None:
                continue

            x1 = source[0] + source[2]
            y1 = source[1] + source[3] / 2

            x2 = target[0]
            y2 = target[1] + target[3] / 2

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=COLORS["accent_light"],
                width=2,
                arrow=tk.LAST
            )

        for mechanic in self._project.mechanics:
            x, y, width, height = positions[
                mechanic.mechanic_id
            ]

            tag = f"node_{mechanic.mechanic_id}"

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
                text=mechanic.name,
                anchor="w",
                fill=COLORS["text_primary"],
                font=FONTS["node"],
                tags=(tag, "node")
            )

            self.canvas.create_text(
                x + 15,
                y + 50,
                text=f"Priority: {mechanic.priority.value}",
                anchor="w",
                fill=COLORS["text_secondary"],
                font=FONTS["small"],
                tags=(tag, "node")
            )

            self.canvas.tag_bind(
                tag,
                "<Button-1>",
                lambda event, item=mechanic: (
                    self._select_mechanic(item)
                )
            )

            self.canvas.tag_bind(
                tag,
                "<ButtonPress-1>",
                lambda event, item=mechanic: (
                    self._start_drag(
                        event,
                        item.mechanic_id
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

    def _select_mechanic(self, mechanic: Mechanic) -> None:
        self._inspector.show_mechanic(mechanic)

    def _start_drag(
        self,
        event,
        mechanic_id: str
    ) -> None:
        self._drag_node_id = mechanic_id
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
                "Mechanics",
                bbox[0],
                bbox[1]
            )

            self._save_callback()

        self._drag_node_id = None
        self._render_flow()

    def _open_add_dialog(self) -> None:
        dialog = ctk.CTkToplevel(self)

        dialog.title("Add Mechanic")
        dialog.geometry("480x450")
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

        name = self._dialog_entry(
            frame,
            "Name"
        )

        ctk.CTkLabel(
            frame,
            text="Priority",
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        priority = ctk.CTkOptionMenu(
            frame,
            values=[item.value for item in Priority]
        )
        priority.pack(
            fill="x",
            padx=20
        )
        priority.set(Priority.MEDIUM.value)

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
                mechanic = Mechanic(
                    name=name.get(),
                    description=description.get(
                        "1.0",
                        "end"
                    ).strip(),
                    priority=Priority(priority.get())
                )

                self._project.add_mechanic(mechanic)
                self._save_callback()

                dialog.destroy()
                self.refresh()

            except (ValueError, TypeError) as exception:
                error.configure(text=str(exception))

        ctk.CTkButton(
            frame,
            text="Add Mechanic",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=add
        ).pack(
            fill="x",
            padx=20,
            pady=15
        )

    def _open_connect_dialog(self) -> None:
        mechanics = self._project.mechanics

        if len(mechanics) < 2:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Connect Mechanics")
        dialog.geometry("430x330")
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

        names = [item.name for item in mechanics]

        ctk.CTkLabel(
            frame,
            text="Source mechanic"
        ).pack(pady=(20, 5))

        source = ctk.CTkOptionMenu(
            frame,
            values=names
        )
        source.pack(
            fill="x",
            padx=20
        )

        ctk.CTkLabel(
            frame,
            text="Target mechanic"
        ).pack(pady=(15, 5))

        target = ctk.CTkOptionMenu(
            frame,
            values=names
        )
        target.pack(
            fill="x",
            padx=20
        )

        error = ctk.CTkLabel(
            frame,
            text="",
            text_color=COLORS["danger"]
        )
        error.pack(pady=8)

        def connect() -> None:
            try:
                source_object = next(
                    item
                    for item in mechanics
                    if item.name == source.get()
                )

                target_object = next(
                    item
                    for item in mechanics
                    if item.name == target.get()
                )

                self._project.connect_mechanics(
                    source_object.mechanic_id,
                    target_object.mechanic_id
                )

                self._save_callback()
                dialog.destroy()
                self.refresh()

            except (ValueError, TypeError) as exception:
                error.configure(text=str(exception))

        ctk.CTkButton(
            frame,
            text="Create Connection",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_dark"],
            command=connect
        ).pack(
            fill="x",
            padx=20,
            pady=10
        )

    @staticmethod
    def _dialog_entry(parent, label: str):
        ctk.CTkLabel(
            parent,
            text=label,
            text_color=COLORS["text_secondary"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        entry = ctk.CTkEntry(parent)
        entry.pack(
            fill="x",
            padx=20
        )

        return entry