from uuid import uuid4


class MechanicConnection:
    def __init__(
        self,
        source_mechanic_id: str,
        target_mechanic_id: str,
        label: str = "",
        connection_id: str | None = None
    ):
        self.connection_id = connection_id or str(uuid4())
        self.source_mechanic_id = source_mechanic_id
        self.target_mechanic_id = target_mechanic_id
        self.label = label

    @property
    def connection_id(self) -> str:
        return self._connection_id

    @connection_id.setter
    def connection_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Connection ID cannot be empty.")

        self._connection_id = value.strip()

    @property
    def source_mechanic_id(self) -> str:
        return self._source_mechanic_id

    @source_mechanic_id.setter
    def source_mechanic_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Source mechanic ID cannot be empty.")

        self._source_mechanic_id = value.strip()

    @property
    def target_mechanic_id(self) -> str:
        return self._target_mechanic_id

    @target_mechanic_id.setter
    def target_mechanic_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Target mechanic ID cannot be empty.")

        self._target_mechanic_id = value.strip()

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Connection label must be a string.")

        self._label = value.strip()

    def to_dict(self) -> dict:
        return {
            "connection_id": self._connection_id,
            "source_mechanic_id": self._source_mechanic_id,
            "target_mechanic_id": self._target_mechanic_id,
            "label": self._label
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MechanicConnection":
        return cls(
            connection_id=data.get("connection_id"),
            source_mechanic_id=data["source_mechanic_id"],
            target_mechanic_id=data["target_mechanic_id"],
            label=data.get("label", "")
        )


class TaskDependency:
    def __init__(
        self,
        prerequisite_task_id: str,
        dependent_task_id: str,
        dependency_id: str | None = None
    ):
        self.dependency_id = dependency_id or str(uuid4())
        self.prerequisite_task_id = prerequisite_task_id
        self.dependent_task_id = dependent_task_id

    @property
    def dependency_id(self) -> str:
        return self._dependency_id

    @dependency_id.setter
    def dependency_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Dependency ID cannot be empty.")

        self._dependency_id = value.strip()

    @property
    def prerequisite_task_id(self) -> str:
        return self._prerequisite_task_id

    @prerequisite_task_id.setter
    def prerequisite_task_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Prerequisite task ID cannot be empty.")

        self._prerequisite_task_id = value.strip()

    @property
    def dependent_task_id(self) -> str:
        return self._dependent_task_id

    @dependent_task_id.setter
    def dependent_task_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Dependent task ID cannot be empty.")

        self._dependent_task_id = value.strip()

    def to_dict(self) -> dict:
        return {
            "dependency_id": self._dependency_id,
            "prerequisite_task_id": self._prerequisite_task_id,
            "dependent_task_id": self._dependent_task_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskDependency":
        return cls(
            dependency_id=data.get("dependency_id"),
            prerequisite_task_id=data["prerequisite_task_id"],
            dependent_task_id=data["dependent_task_id"]
        )


class TaskMechanicLink:
    def __init__(
        self,
        task_id: str,
        mechanic_id: str
    ):
        self.task_id = task_id
        self.mechanic_id = mechanic_id

    @property
    def task_id(self) -> str:
        return self._task_id

    @task_id.setter
    def task_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task ID cannot be empty.")

        self._task_id = value.strip()

    @property
    def mechanic_id(self) -> str:
        return self._mechanic_id

    @mechanic_id.setter
    def mechanic_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Mechanic ID cannot be empty.")

        self._mechanic_id = value.strip()

    def to_dict(self) -> dict:
        return {
            "task_id": self._task_id,
            "mechanic_id": self._mechanic_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskMechanicLink":
        return cls(
            task_id=data["task_id"],
            mechanic_id=data["mechanic_id"]
        )