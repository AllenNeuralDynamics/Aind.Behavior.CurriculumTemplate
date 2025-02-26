import os
from typing import Callable, Literal, TypeVar, Union

# This curriculum only has 2 stages and a single transition from stage 1 to stage 2
# The first stage has a single policy that update suggestions while stage 1 is active
from aind_behavior_curriculum import (
    Metrics,
    MetricsProvider,
    Policy,
    Stage,
    StageTransition,
    TaskParameters,
    Trainer,
    TrainerState,
    create_curriculum,
)

from aind_behavior_curriculum_template import __version__
from aind_behavior_curriculum_template.metrics import TemplateMetrics, metrics_from_dataset
from aind_behavior_curriculum_template.task_logic import TemplateParameters, TemplateTaskLogic

from .utils import model_from_json_file

# ============================================================
# I suggest the following naming convention to keep things clear:
# - Policies should start with "p_" (e.g. p_identity_policy)
# - Policy transitions should start with "pt_"
# - Stages should start with "s_" (e.g. s_stage1)
# - Stage transitions should start with "st_" and should be named
#   after the stages they transition between (e.g. st_s_stage1_s_stage2)
# ============================================================


# ============================================================
# Policies to update task parameters based on metrics
# ============================================================

# Useful type hints for generic policies
TMetrics = TypeVar("TMetrics", bound=Metrics)
TTaskParameters = TypeVar("TTaskParameters", bound=TaskParameters)
PolicyType = Callable[[TMetrics, TTaskParameters], TTaskParameters]  # This should generally work for type hinting


def p_identity_policy(metrics: TMetrics, task_parameters: TTaskParameters) -> TTaskParameters:  # pylint: disable=W0613
    """An identity policy that does nothing"""
    return task_parameters


def p_set_mode_from_metric1(metrics: TemplateMetrics, task_parameters: TemplateParameters) -> TemplateParameters:
    if metrics.metric1 < 0:
        task_parameters.mode = "foo"
    elif 0 <= metrics.metric1 < 0.5:
        task_parameters.mode = "bar"
    else:
        task_parameters.mode = "baz"

    return task_parameters


# ============================================================
# Stage transitions
# ============================================================


def st_s_stage_a_s_stage_b(metrics: TemplateMetrics) -> bool:
    return metrics.metric1 > 1


# ============================================================
# Curriculum definition
# ============================================================


class AnotherTask(TemplateTaskLogic):
    name: Literal["AnotherTask"] = "AnotherTask"


curriculum_class = create_curriculum("TemplateCurriculum", __version__, (TemplateTaskLogic, AnotherTask))
curriculum = curriculum_class()

s_stage_a = Stage(
    name="stage_a",
    task=TemplateTaskLogic(task_parameters=TemplateParameters(mode="foo")),
    start_policies=[Policy(x) for x in [p_set_mode_from_metric1]],
    metrics_provider=MetricsProvider(metrics_from_dataset),
)

s_stage_b = Stage(
    name="stage_b",
    task=TemplateTaskLogic(task_parameters=TemplateParameters(mode="bar")),
    metrics_provider=MetricsProvider(metrics_from_dataset),
)

curriculum.add_stage_transition(s_stage_a, s_stage_b, StageTransition(st_s_stage_a_s_stage_b))


# ==============================================================================
# Create a Trainer that uses the curriculum to bootstrap suggestions
# ==============================================================================

TRAINER = Trainer(curriculum)


def get_trainer_state(path: Union[str, os.PathLike], trainer: Trainer = TRAINER) -> TrainerState:
    return model_from_json_file(path, trainer._trainer_state_factory)


TTrainerState = TypeVar("TTrainerState", bound=TrainerState)


def get_metrics(path: Union[str, os.PathLike], trainer_state: TTrainerState) -> Metrics:
    stage = trainer_state.stage
    if stage is None:
        raise ValueError("Trainer state does not have a stage")
    if stage.metrics_provider is None:
        raise ValueError("Stage does not have a metrics provider")
    metrics_provider = stage.metrics_provider
    return metrics_provider.callable(path)
