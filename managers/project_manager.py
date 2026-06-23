from managers.file_manager import FileManager
from models.game_project import GameProject


class ProjectManager:
    def __init__(self, file_manager: FileManager | None = None):
        self._file_manager = file_manager or FileManager()
        self._projects: list[GameProject] = self._file_manager.load_projects()

    @property
    def projects(self) -> list[GameProject]:
        return self._projects.copy()

    def add_project(self, project: GameProject) -> None:
        if not isinstance(project, GameProject):
            raise TypeError("Only GameProject objects can be added.")

        if self.find_project(project.name) is not None:
            raise ValueError(
                f'A project named "{project.name}" already exists.'
            )

        self._projects.append(project)
        self.save()

    def find_project(self, name: str) -> GameProject | None:
        if not isinstance(name, str):
            raise TypeError("Project name must be a string.")

        searched_name = name.strip().lower()

        for project in self._projects:
            if project.name.lower() == searched_name:
                return project

        return None

    def remove_project(self, name: str) -> bool:
        project = self.find_project(name)

        if project is None:
            return False

        self._projects.remove(project)
        self.save()
        return True

    def get_projects_by_status(self, status) -> list[GameProject]:
        return [
            project
            for project in self._projects
            if project.status == status
        ]

    def save(self) -> None:
        self._file_manager.save_projects(self._projects)