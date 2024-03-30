from enumfields import Enum


class WorkType(str, Enum):
    office = "1"
    remote = "2"
    hybrid = "3"


class JobStatus(str, Enum):
    new = "1"
    viewed = "2"
    applied = "3"
    ignored = "4"
