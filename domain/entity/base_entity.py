import uuid

from dataclasses import asdict, dataclass, field
from datetime import datetime


@dataclass
class BaseEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
