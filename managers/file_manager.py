import json
from pathlib import Path

from models.game_project import GameProject


class FileManager:
    def __init__(self, file_path: str = "data/projects.json"):
        self._file_path = Path(file_path)

    @property
    def file_path(self) -> Path:
        return self._file_path

    def save_projects(self, projects: list[GameProject]) -> None:
        if not isinstance(projects, list):
            raise TypeError("Projects must be provided as a list.")

        for project in projects:
            if not isinstance(project, GameProject):
                raise TypeError(
                    "The projects list must contain only GameProject objects."
                )

        self._file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = [
            project.to_dict()
            for project in projects
        ]

        with self._file_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def load_projects(self) -> list[GameProject]:
        if not self._file_path.exists():
            return []

        try:
            with self._file_path.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The projects file contains invalid JSON."
            ) from error

        if not isinstance(data, list):
            raise ValueError(
                "The projects file must contain a list."
            )

        return [
            GameProject.from_dict(project_data)
            for project_data in data
        ]