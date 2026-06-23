from uuid import uuid4

from models.enums import Priority


class Mechanic:
    def __init__(
        self,
        name: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        mechanic_id: str | None = None
    ):
        self.mechanic_id = mechanic_id or str(uuid4())
        self.name = name
        self.description = description
        self.priority = priority

    @property
    def mechanic_id(self) -> str:
        return self._mechanic_id

    @mechanic_id.setter
    def mechanic_id(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Mechanic ID must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Mechanic ID cannot be empty.")

        self._mechanic_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Mechanic name must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Mechanic name cannot be empty.")

        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Mechanic description must be a string.")

        self._description = value.strip()

    @property
    def priority(self) -> Priority:
        return self._priority

    @priority.setter
    def priority(self, value: Priority) -> None:
        if not isinstance(value, Priority):
            raise TypeError("Mechanic priority must be a Priority value.")

        self._priority = value

    def to_dict(self) -> dict:
        return {
            "mechanic_id": self._mechanic_id,
            "name": self._name,
            "description": self._description,
            "priority": self._priority.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Mechanic":
        if not isinstance(data, dict):
            raise TypeError("Mechanic data must be a dictionary.")

        return cls(
            mechanic_id=data.get("mechanic_id"),
            name=data["name"],
            description=data.get("description", ""),
            priority=Priority(
                data.get("priority", Priority.MEDIUM.value)
            )
        )

    def __str__(self) -> str:
        return f"{self._name} | {self._priority.value}"