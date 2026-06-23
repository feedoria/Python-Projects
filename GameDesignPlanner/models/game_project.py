from models.asset import Asset
from models.enums import ProjectStatus, TaskStatus
from models.layout import NodeLayout
from models.mechanic import Mechanic
from models.relationships import (
    MechanicConnection,
    TaskDependency,
    TaskMechanicLink
)
from models.task import Task
from models.technology import Technology


class GameProject:
    def __init__(
        self,
        name: str,
        genre: str,
        description: str = "",
        platform: str = "PC",
        status: ProjectStatus = ProjectStatus.IDEA,
        difficulty: int = 1
    ):
        self.name = name
        self.genre = genre
        self.description = description
        self.platform = platform
        self.status = status
        self.difficulty = difficulty

        self._tasks: list[Task] = []
        self._mechanics: list[Mechanic] = []
        self._assets: list[Asset] = []
        self._technologies: list[Technology] = []

        self._mechanic_connections: list[MechanicConnection] = []
        self._task_dependencies: list[TaskDependency] = []
        self._task_mechanic_links: list[TaskMechanicLink] = []
        self._node_layouts: list[NodeLayout] = []

    # --------------------
    # Basic properties
    # --------------------

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Project name must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Project name cannot be empty.")

        self._name = value

    @property
    def genre(self) -> str:
        return self._genre

    @genre.setter
    def genre(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Genre must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Genre cannot be empty.")

        self._genre = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Description must be a string.")

        self._description = value.strip()

    @property
    def platform(self) -> str:
        return self._platform

    @platform.setter
    def platform(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Platform must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Platform cannot be empty.")

        self._platform = value

    @property
    def status(self) -> ProjectStatus:
        return self._status

    @status.setter
    def status(self, value: ProjectStatus) -> None:
        if not isinstance(value, ProjectStatus):
            raise TypeError("Status must be a ProjectStatus value.")

        self._status = value

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Difficulty must be an integer.")

        if not 1 <= value <= 10:
            raise ValueError("Difficulty must be between 1 and 10.")

        self._difficulty = value

    # --------------------
    # Collection properties
    # --------------------

    @property
    def tasks(self) -> list[Task]:
        return self._tasks.copy()

    @property
    def mechanics(self) -> list[Mechanic]:
        return self._mechanics.copy()

    @property
    def assets(self) -> list[Asset]:
        return self._assets.copy()

    @property
    def technologies(self) -> list[Technology]:
        return self._technologies.copy()

    @property
    def mechanic_connections(self) -> list[MechanicConnection]:
        return self._mechanic_connections.copy()

    @property
    def task_dependencies(self) -> list[TaskDependency]:
        return self._task_dependencies.copy()

    @property
    def task_mechanic_links(self) -> list[TaskMechanicLink]:
        return self._task_mechanic_links.copy()

    @property
    def node_layouts(self) -> list[NodeLayout]:
        return self._node_layouts.copy()

    # --------------------
    # Add elements
    # --------------------

    def add_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Only Task objects can be added.")

        if self.find_task(task.task_id) is not None:
            raise ValueError("A task with this ID already exists.")

        self._tasks.append(task)

    def add_mechanic(self, mechanic: Mechanic) -> None:
        if not isinstance(mechanic, Mechanic):
            raise TypeError("Only Mechanic objects can be added.")

        if self.find_mechanic(mechanic.mechanic_id) is not None:
            raise ValueError("A mechanic with this ID already exists.")

        self._mechanics.append(mechanic)

    def add_asset(self, asset: Asset) -> None:
        if not isinstance(asset, Asset):
            raise TypeError("Only Asset objects can be added.")

        self._assets.append(asset)

    def add_technology(self, technology: Technology) -> None:
        if not isinstance(technology, Technology):
            raise TypeError("Only Technology objects can be added.")

        self._technologies.append(technology)

    # --------------------
    # Find elements
    # --------------------

    def find_task(self, task_id: str) -> Task | None:
        for task in self._tasks:
            if task.task_id == task_id:
                return task

        return None

    def find_mechanic(self, mechanic_id: str) -> Mechanic | None:
        for mechanic in self._mechanics:
            if mechanic.mechanic_id == mechanic_id:
                return mechanic

        return None

    def find_layout(
        self,
        node_id: str,
        view_name: str
    ) -> NodeLayout | None:
        for layout in self._node_layouts:
            if (
                layout.node_id == node_id
                and layout.view_name == view_name
            ):
                return layout

        return None

    # --------------------
    # Mechanic connections
    # --------------------

    def connect_mechanics(
        self,
        source_mechanic_id: str,
        target_mechanic_id: str,
        label: str = ""
    ) -> None:
        if source_mechanic_id == target_mechanic_id:
            raise ValueError("A mechanic cannot connect to itself.")

        if self.find_mechanic(source_mechanic_id) is None:
            raise ValueError("Source mechanic does not exist.")

        if self.find_mechanic(target_mechanic_id) is None:
            raise ValueError("Target mechanic does not exist.")

        for connection in self._mechanic_connections:
            if (
                connection.source_mechanic_id == source_mechanic_id
                and connection.target_mechanic_id == target_mechanic_id
            ):
                raise ValueError("This mechanic connection already exists.")

        connection = MechanicConnection(
            source_mechanic_id=source_mechanic_id,
            target_mechanic_id=target_mechanic_id,
            label=label
        )

        self._mechanic_connections.append(connection)

    def remove_mechanic_connection(
        self,
        connection_id: str
    ) -> bool:
        for connection in self._mechanic_connections:
            if connection.connection_id == connection_id:
                self._mechanic_connections.remove(connection)
                return True

        return False

    # --------------------
    # Task dependencies
    # --------------------

    def add_task_dependency(
        self,
        prerequisite_task_id: str,
        dependent_task_id: str
    ) -> None:
        if prerequisite_task_id == dependent_task_id:
            raise ValueError("A task cannot depend on itself.")

        if self.find_task(prerequisite_task_id) is None:
            raise ValueError("Prerequisite task does not exist.")

        if self.find_task(dependent_task_id) is None:
            raise ValueError("Dependent task does not exist.")

        for dependency in self._task_dependencies:
            if (
                dependency.prerequisite_task_id == prerequisite_task_id
                and dependency.dependent_task_id == dependent_task_id
            ):
                raise ValueError("This task dependency already exists.")

        dependency = TaskDependency(
            prerequisite_task_id=prerequisite_task_id,
            dependent_task_id=dependent_task_id
        )

        self._task_dependencies.append(dependency)

    def remove_task_dependency(
        self,
        dependency_id: str
    ) -> bool:
        for dependency in self._task_dependencies:
            if dependency.dependency_id == dependency_id:
                self._task_dependencies.remove(dependency)
                return True

        return False

    # --------------------
    # Task-mechanic links
    # --------------------

    def link_task_to_mechanic(
        self,
        task_id: str,
        mechanic_id: str
    ) -> None:
        if self.find_task(task_id) is None:
            raise ValueError("Task does not exist.")

        if self.find_mechanic(mechanic_id) is None:
            raise ValueError("Mechanic does not exist.")

        for link in self._task_mechanic_links:
            if (
                link.task_id == task_id
                and link.mechanic_id == mechanic_id
            ):
                return

        self._task_mechanic_links.append(
            TaskMechanicLink(
                task_id=task_id,
                mechanic_id=mechanic_id
            )
        )

    def unlink_task_from_mechanic(
        self,
        task_id: str,
        mechanic_id: str
    ) -> bool:
        for link in self._task_mechanic_links:
            if (
                link.task_id == task_id
                and link.mechanic_id == mechanic_id
            ):
                self._task_mechanic_links.remove(link)
                return True

        return False

    # --------------------
    # Node layout
    # --------------------

    def set_node_layout(
        self,
        node_id: str,
        view_name: str,
        position_x: float,
        position_y: float,
        width: float = 180.0,
        height: float = 90.0
    ) -> None:
        existing_layout = self.find_layout(node_id, view_name)

        if existing_layout is not None:
            existing_layout.move_to(position_x, position_y)
            existing_layout.width = width
            existing_layout.height = height
            return

        self._node_layouts.append(
            NodeLayout(
                node_id=node_id,
                view_name=view_name,
                position_x=position_x,
                position_y=position_y,
                width=width,
                height=height
            )
        )

    # --------------------
    # Delete elements
    # --------------------

    def remove_task(self, task_id: str) -> bool:
        task = self.find_task(task_id)

        if task is None:
            return False

        self._tasks.remove(task)

        self._task_dependencies = [
            dependency
            for dependency in self._task_dependencies
            if (
                dependency.prerequisite_task_id != task_id
                and dependency.dependent_task_id != task_id
            )
        ]

        self._task_mechanic_links = [
            link
            for link in self._task_mechanic_links
            if link.task_id != task_id
        ]

        self._node_layouts = [
            layout
            for layout in self._node_layouts
            if layout.node_id != task_id
        ]

        return True

    def remove_mechanic(self, mechanic_id: str) -> bool:
        mechanic = self.find_mechanic(mechanic_id)

        if mechanic is None:
            return False

        self._mechanics.remove(mechanic)

        self._mechanic_connections = [
            connection
            for connection in self._mechanic_connections
            if (
                connection.source_mechanic_id != mechanic_id
                and connection.target_mechanic_id != mechanic_id
            )
        ]

        self._task_mechanic_links = [
            link
            for link in self._task_mechanic_links
            if link.mechanic_id != mechanic_id
        ]

        self._node_layouts = [
            layout
            for layout in self._node_layouts
            if layout.node_id != mechanic_id
        ]

        return True

    # --------------------
    # Statistics
    # --------------------

    def calculate_progress(self) -> float:
        if not self._tasks:
            return 0.0

        completed_tasks = sum(
            1
            for task in self._tasks
            if task.status == TaskStatus.DONE
        )

        return round(
            completed_tasks / len(self._tasks) * 100,
            2
        )

    def calculate_remaining_hours(self) -> float:
        return round(
            sum(
                task.estimated_hours
                for task in self._tasks
                if not task.is_completed()
            ),
            2
        )

    # --------------------
    # JSON conversion
    # --------------------

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "genre": self._genre,
            "description": self._description,
            "platform": self._platform,
            "status": self._status.value,
            "difficulty": self._difficulty,

            "tasks": [
                task.to_dict()
                for task in self._tasks
            ],

            "mechanics": [
                mechanic.to_dict()
                for mechanic in self._mechanics
            ],

            "assets": [
                asset.to_dict()
                for asset in self._assets
            ],

            "technologies": [
                technology.to_dict()
                for technology in self._technologies
            ],

            "mechanic_connections": [
                connection.to_dict()
                for connection in self._mechanic_connections
            ],

            "task_dependencies": [
                dependency.to_dict()
                for dependency in self._task_dependencies
            ],

            "task_mechanic_links": [
                link.to_dict()
                for link in self._task_mechanic_links
            ],

            "node_layouts": [
                layout.to_dict()
                for layout in self._node_layouts
            ]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameProject":
        if not isinstance(data, dict):
            raise TypeError("Project data must be a dictionary.")

        project = cls(
            name=data["name"],
            genre=data["genre"],
            description=data.get("description", ""),
            platform=data.get("platform", "PC"),
            status=ProjectStatus(
                data.get(
                    "status",
                    ProjectStatus.IDEA.value
                )
            ),
            difficulty=data.get("difficulty", 1)
        )

        for task_data in data.get("tasks", []):
            project.add_task(
                Task.from_dict(task_data)
            )

        for mechanic_data in data.get("mechanics", []):
            project.add_mechanic(
                Mechanic.from_dict(mechanic_data)
            )

        for asset_data in data.get("assets", []):
            project.add_asset(
                Asset.from_dict(asset_data)
            )

        for technology_data in data.get("technologies", []):
            project.add_technology(
                Technology.from_dict(technology_data)
            )

        for connection_data in data.get(
            "mechanic_connections",
            []
        ):
            project._mechanic_connections.append(
                MechanicConnection.from_dict(connection_data)
            )

        for dependency_data in data.get(
            "task_dependencies",
            []
        ):
            project._task_dependencies.append(
                TaskDependency.from_dict(dependency_data)
            )

        for link_data in data.get(
            "task_mechanic_links",
            []
        ):
            project._task_mechanic_links.append(
                TaskMechanicLink.from_dict(link_data)
            )

        for layout_data in data.get("node_layouts", []):
            project._node_layouts.append(
                NodeLayout.from_dict(layout_data)
            )

        return project

    def __str__(self) -> str:
        return (
            f"{self._name} | "
            f"{self._genre} | "
            f"{self._status.value} | "
            f"Progress: {self.calculate_progress()}%"
        )