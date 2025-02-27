import os
from typing import List

from aind_behavior_curriculum import Metrics
from pydantic import Field


class TemplateMetrics(Metrics):
    metric1: float
    metric2_history: List[float] = Field(default_factory=list)


def metrics_from_dataset(data_directory: os.PathLike) -> TemplateMetrics:  # pylint: disable=W0613
    # Load dataset and calculate metrics here
    return TemplateMetrics(metric1=1.0, metric2_history=[1.0, 2.0, 3.0])
