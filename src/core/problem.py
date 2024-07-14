from typing import Optional, List, Union

from omegaconf import OmegaConf
from pydantic import BaseModel

from src.core.tasks import Task


class Problem(BaseModel):
    lines: str
    vim_lines: Optional[str] = None


class Lesson(BaseModel):
    plan: str
    problems: List[Problem] | None = None


class Strategy(BaseModel):
    lesson: Union[List[Task], Task]

    @classmethod
    def from_yaml(cls, path: str) -> 'Strategy':
        cfg = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**cfg)
