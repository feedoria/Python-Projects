from uuid import uuid4

from models.enums import Priority, TaskStatus


class Task:
    def __init__(
        self,
        title: str,
        description: str = "",
        status: TaskStatus = TaskStatus.NOT_STARTED,
        difficulty: int = 1,
        priority: Priority = Priority.MEDIUM,
        estimated_hours: float = 0.0,
        task_id: str | None = None
    ):
        self.task_id = task_id or str(uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.difficulty = difficulty
        self.priority = priority
        self.estimated_hours = estimated_hours

    @property
    def task_id(self) -> str:
        return self._task_id

    @task_id.setter
    def task_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Task ID must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Task ID cannot be empty.")

        self._task_id = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Task title must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty.")

        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Task description must be a string.")

        self._description = value.strip()

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, value: TaskStatus) -> None:
        if not isinstance(value, TaskStatus):
            raise TypeError("Task status must be a TaskStatus value.")

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

    @property
    def priority(self) -> Priority:
        return self._priority

    @priority.setter
    def priority(self, value: Priority) -> None:
        if not isinstance(value, Priority):
            raise TypeError("Task priority must be a Priority value.")

        self._priority = value

    @property
    def estimated_hours(self) -> float:
        return self._estimated_hours

    @estimated_hours.setter
    def estimated_hours(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Estimated hours must be a number.")

        value = float(value)

        if value < 0:
            raise ValueError("Estimated hours cannot be negative.")

        self._estimated_hours = value

    def is_completed(self) -> bool:
        return self._status == TaskStatus.DONE

    def to_dict(self) -> dict:
        return {
            "task_id": self._task_id,
            "title": self._title,
            "description": self._description,
            "status": self._status.value,
            "difficulty": self._difficulty,
            "priority": self._priority.value,
            "estimated_hours": self._estimated_hours
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        if not isinstance(data, dict):
            raise TypeError("Task data must be a dictionary.")

        return cls(
            task_id=data.get("task_id"),
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(
                data.get("status", TaskStatus.NOT_STARTED.value)
            ),
            difficulty=data.get("difficulty", 1),
            priority=Priority(
                data.get("priority", Priority.MEDIUM.value)
            ),
            estimated_hours=data.get("estimated_hours", 0.0)
        )

    def __str__(self) -> str:
        return (
            f"{self._title} | "
            f"{self._status.value} | "
            f"{self._priority.value}"
        )