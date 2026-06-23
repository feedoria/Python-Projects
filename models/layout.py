class NodeLayout:
    VALID_VIEWS = ["Mechanics", "Tasks"]

    def __init__(
        self,
        node_id: str,
        view_name: str,
        position_x: float = 100.0,
        position_y: float = 100.0,
        width: float = 180.0,
        height: float = 90.0
    ):
        self.node_id = node_id
        self.view_name = view_name
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height

    @property
    def node_id(self) -> str:
        return self._node_id

    @node_id.setter
    def node_id(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Node ID cannot be empty.")

        self._node_id = value.strip()

    @property
    def view_name(self) -> str:
        return self._view_name

    @view_name.setter
    def view_name(self, value: str) -> None:
        if value not in self.VALID_VIEWS:
            raise ValueError(
                f"View name must be one of: {', '.join(self.VALID_VIEWS)}"
            )

        self._view_name = value

    @property
    def position_x(self) -> float:
        return self._position_x

    @position_x.setter
    def position_x(self, value: float) -> None:
        self._position_x = self._validate_number(value, "Position X")

    @property
    def position_y(self) -> float:
        return self._position_y

    @position_y.setter
    def position_y(self, value: float) -> None:
        self._position_y = self._validate_number(value, "Position Y")

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        value = self._validate_number(value, "Width")

        if value <= 0:
            raise ValueError("Width must be greater than zero.")

        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        value = self._validate_number(value, "Height")

        if value <= 0:
            raise ValueError("Height must be greater than zero.")

        self._height = value

    @staticmethod
    def _validate_number(value: float, field_name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a number.")

        return float(value)

    def move_to(self, position_x: float, position_y: float) -> None:
        self.position_x = position_x
        self.position_y = position_y

    def to_dict(self) -> dict:
        return {
            "node_id": self._node_id,
            "view_name": self._view_name,
            "position_x": self._position_x,
            "position_y": self._position_y,
            "width": self._width,
            "height": self._height
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NodeLayout":
        return cls(
            node_id=data["node_id"],
            view_name=data["view_name"],
            position_x=data.get("position_x", 100.0),
            position_y=data.get("position_y", 100.0),
            width=data.get("width", 180.0),
            height=data.get("height", 90.0)
        )