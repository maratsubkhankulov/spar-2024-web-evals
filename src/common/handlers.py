import importlib
import os
import shutil
from typing import Any

from pydantic import BaseModel

from src.core.tasks import Task


def load_object(obj_path: str, default_obj_path: str = '') -> callable:
    obj_path_list = obj_path.rsplit('.', 1)
    obj_path = obj_path_list.pop(0) if len(obj_path_list) > 1 else default_obj_path
    obj_name = obj_path_list[0]
    module_obj = importlib.import_module(obj_path)
    if not hasattr(module_obj, obj_name):  # noqa: WPS421
        raise AttributeError(f'Object `{obj_name}` cannot be loaded from `{obj_path}`.')
    returned_class = getattr(module_obj, obj_name)
    return returned_class if returned_class else callable


def dump_file(file_path: str, dump_folder: str = '/app/data/dump') -> str:
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)

    file_name = os.path.basename(file_path)
    dump_file_path = os.path.join(dump_folder, file_name)
    shutil.copy(file_path, dump_file_path)

    return dump_file_path


def load_created_object(obj_path: str, kwargs: dict) -> Any:
    class_object = load_object(obj_path)
    return class_object(**kwargs)


def write_file(path: str, content: bytes, rewrite: bool = False):
    if not os.path.exists(path) or rewrite:
        with open(path, 'wb') as file_:
            file_.write(content)


def jsonize(function):
    """
    Decorator for json serialization
    :param function: function which outputs BaseModel object
    :return: decorated version of the function with jsonized return value
    """

    def wrapper(*args, **kwargs):
        output = function(*args, **kwargs)
        return output if not isinstance(output, BaseModel) else output.model_dump_json()

    return wrapper


make_dummy_task = lambda steps: Task(question="1+1", steps=steps, name="__dummy__")  # noqa: E731
