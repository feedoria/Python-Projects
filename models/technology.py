class Technology:
    def __init__(
        self,
        name: str,
        category: str = "",
        notes: str = ""
    ):
        self.name = name
        self.category = category
        self.notes = notes

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Technology name must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Technology name cannot be empty.")

        self._name = value

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Technology category must be a string.")

        self._category = value.strip()

    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Technology notes must be a string.")

        self._notes = value.strip()

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "category": self._category,
            "notes": self._notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Technology":
        if not isinstance(data, dict):
            raise TypeError("Technology data must be a dictionary.")

        return cls(
            name=data["name"],
            category=data.get("category", ""),
            notes=data.get("notes", "")
        )

    def __str__(self) -> str:
        if self._category:
            return f"{self._name} | {self._category}"

        return self._name