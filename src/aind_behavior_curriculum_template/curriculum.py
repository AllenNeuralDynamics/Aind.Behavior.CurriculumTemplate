from typing import Callable, Literal, TypeVar

# This curriculum only has 2 stages and a single transition from stage 1 to stage 2
# The first stage has a single policy that update suggestions while stage 1 is active
from aind_behavior_curriculum import Metrics, Policy, Stage, TaskParameters, Trainer, create_curriculum
from pydantic import Field

from aind_behavior_curriculum_template import __version__
from aind_behavior_curriculum_template.metrics import TemplateMetrics
from aind_behavior_curriculum_template.task_logic import TemplateParameters, TemplateTaskLogic

# ============================================================
# I suggest the following naming convention to keep things clear:
# - Policies should start with "p_" (e.g. p_identity_policy)
# - Stage transitions should start with "st_" and should be named
#   after the stages they transition between (e.g. st_stage1_to_stage2)
# - Policy transitions should start with "pt_"
# - Stages should start with "s_" (e.g. s_stage1)
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

StageTransition = Callable[[TMetrics], bool]


def st_stage_a_to_stage_b(metrics: TemplateMetrics) -> bool:
    return metrics.metric1 > 1


# ============================================================
# Curriculum definition
# ============================================================


class AnotherTask(TemplateTaskLogic):
    name: Literal["AnotherTask"] = Field(default="AnotherTask")


curriculum_class = create_curriculum("TemplateCurriculum", __version__, (TemplateTaskLogic, AnotherTask))
curriculum = curriculum_class()

s_stage_a = Stage(
    name="stage_a",
    task=TemplateTaskLogic(task_parameters=TemplateParameters(mode="foo")),
    start_policies=[Policy(rule=x) for x in [p_set_mode_from_metric1]],
)

s_stage_b = Stage(
    name="stage_b",
    task=TemplateTaskLogic(task_parameters=TemplateParameters(mode="bar")),
)

curriculum.add_stage_transition(s_stage_a, s_stage_b, st_stage_a_to_stage_b)


# ==============================================================================
# Create a Trainer that uses the curriculum to bootstrap suggestions
# ==============================================================================

trainer = Trainer(curriculum)
