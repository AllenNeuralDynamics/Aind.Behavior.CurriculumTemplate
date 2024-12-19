from typing import Literal

from aind_behavior_curriculum.task import Task, TaskParameters
from pydantic import Field


class TemplateParameters(TaskParameters):
    example_parameter: float = Field(default=1.0, description="An example parameter")
    mode: Literal["foo", "bar", "baz"]


class TemplateTaskLogic(Task):
    name: Literal["TemplateTask"] = Field(default="TemplateTask")
    version: Literal["0.0.0"] = Field(default="0.0.0", description="The version of the task", frozen=True)
    task_parameters: TemplateParameters = Field(
        default_factory=TemplateParameters, description="The parameters of the task"
    )
    description: str = Field(default="A template task", description="A description of the task. This one does nothing.")
