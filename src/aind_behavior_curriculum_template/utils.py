import os
import pathlib
import typing

import pydantic

TModel = typing.TypeVar("TModel", bound=pydantic.BaseModel)


def model_from_json_file(json_path: os.PathLike | str, model: type[TModel]) -> TModel:
    with open(pathlib.Path(json_path), "r", encoding="utf-8") as file:
        return model.model_validate_json(file.read())
