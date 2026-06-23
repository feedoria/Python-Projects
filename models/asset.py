from models.enums import AssetStatus, AssetType


class Asset:
    def __init__(
        self,
        name: str,
        asset_type: AssetType = AssetType.OTHER,
        status: AssetStatus = AssetStatus.NEEDED,
        description: str = ""
    ):
        self.name = name
        self.asset_type = asset_type
        self.status = status
        self.description = description

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Asset name must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Asset name cannot be empty.")

        self._name = value

    @property
    def asset_type(self) -> AssetType:
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value: AssetType) -> None:
        if not isinstance(value, AssetType):
            raise TypeError("Asset type must be an AssetType value.")

        self._asset_type = value

    @property
    def status(self) -> AssetStatus:
        return self._status

    @status.setter
    def status(self, value: AssetStatus) -> None:
        if not isinstance(value, AssetStatus):
            raise TypeError("Asset status must be an AssetStatus value.")

        self._status = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Asset description must be a string.")

        self._description = value.strip()

    def is_ready(self) -> bool:
        return self._status == AssetStatus.READY

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "asset_type": self._asset_type.value,
            "status": self._status.value,
            "description": self._description
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Asset":
        if not isinstance(data, dict):
            raise TypeError("Asset data must be a dictionary.")

        return cls(
            name=data["name"],
            asset_type=AssetType(
                data.get("asset_type", AssetType.OTHER.value)
            ),
            status=AssetStatus(
                data.get("status", AssetStatus.NEEDED.value)
            ),
            description=data.get("description", "")
        )

    def __str__(self) -> str:
        return (
            f"{self._name} | "
            f"{self._asset_type.value} | "
            f"{self._status.value}"
        )