from enum import Enum


class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class AssetType(Enum):
    MODEL_3D = "3D Model"
    TEXTURE = "Texture"
    AUDIO = "Audio"
    UI = "UI"
    ANIMATION = "Animation"
    OTHER = "Other"


class AssetStatus(Enum):
    NEEDED = "Needed"
    IN_PROGRESS = "In Progress"
    READY = "Ready"

class ProjectStatus(Enum):
    IDEA = "Idea"
    PLANNING = "Planning"
    IN_DEVELOPMENT = "In Development"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"