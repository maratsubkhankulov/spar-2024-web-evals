from typing import Optional, List, Union, ForwardRef
from pydantic import BaseModel


class Instruction(BaseModel):
    template: str
    head: str
    fewshot: str = ''
    tail: str

    def update(self, **new_data):
        for field, value in new_data.items():
            setattr(self, field, value)


class VimInstruction(Instruction):
    str_sample: str = ''


class MechanicPromptTemplate(BaseModel):
    instruction: Instruction
    vim_instruction: Optional[VimInstruction] = None


Task = ForwardRef('Task')


class Task(BaseModel):  # noqa: WPS440  The reference above is necessary for the fractal structure
    question: str
    steps: Union[List[Task], Task] = None
    name: str = 'task_name'
    kwargs: dict = {}
    priority_model: Optional[str] = None
    parse: Union[str, None] = None
