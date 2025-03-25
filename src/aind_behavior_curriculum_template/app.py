from __future__ import annotations

from pathlib import Path

import aind_behavior_curriculum
from pydantic_settings import CliApp

import aind_behavior_curriculum_template
from aind_behavior_curriculum_template import logger
from aind_behavior_curriculum_template.curriculum import get_metrics, get_trainer_state
from aind_behavior_curriculum_template.utils import CurriculumAppCliArgs, CurriculumCliArgs, CurriculumCliOutput


def run_curriculum(args: CurriculumCliArgs):
    if not args.data_directory == Path("demo"):
        trainer_state = get_trainer_state(args.input_trainer_state)
        metrics = get_metrics(args.data_directory, trainer_state)
    else:
        # This is a demo mode for unittest only
        from aind_behavior_curriculum_template.curriculum import (
            TRAINER,
            Policy,
            TemplateMetrics,
            p_set_mode_from_metric1,
            s_stage_a,
        )

        trainer_state = TRAINER.create_trainer_state(
            stage=s_stage_a,
            is_on_curriculum=True,
            active_policies=tuple([Policy(x) for x in [p_set_mode_from_metric1]]),
        )
        metrics = TemplateMetrics(metric1=50, metric2_history=[1.0, 2.0, 3.0])

    # Compute suggestion
    suggestion = TRAINER.evaluate(trainer_state, metrics)

    output = CurriculumCliOutput(
        trainer_state=suggestion,
        metrics=metrics,
        abc_version=aind_behavior_curriculum.__version__,
        version=aind_behavior_curriculum_template.__version__,
    )
    if not args.mute_output:
        logger.info(output.model_dump_json())

    if args.output_suggestion is not None:
        with open(Path(args.output_suggestion) / "suggestion.json", "w", encoding="utf-8") as file:
            file.write(suggestion.model_dump_json(indent=2))

    if args.output_metrics is not None:
        with open(Path(args.output_metrics) / "metrics.json", "w", encoding="utf-8") as file:
            file.write(metrics.model_dump_json(indent=2))


def main():
    args = CliApp.run(CurriculumAppCliArgs)
    if args.run is not None:
        run_curriculum(args.run)
    if args.abc_version:
        logger.info(aind_behavior_curriculum_template.__version__)
    if args.version:
        logger.info(aind_behavior_curriculum.__version__)


if __name__ == "__main__":
    main()
