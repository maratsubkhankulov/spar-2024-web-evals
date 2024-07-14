from omegaconf import OmegaConf
from pydantic import BaseModel


class Config(BaseModel):
    lesson: dict
    mechanics: dict

    @classmethod
    def from_yaml(cls, path: str) -> 'Config':
        cfg = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**cfg)
