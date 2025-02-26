from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import aind_behavior_curriculum
import click

import aind_behavior_curriculum_template
from aind_behavior_curriculum_template.curriculum import get_metrics, get_trainer_state

logger = logging.getLogger(__name__)


@dataclass
class CliArgs:
    data_directory: str | os.PathLike
    input_trainer_state: str | os.PathLike
    mute_trainer_state: bool = False
    mute_metrics: bool = False
    output_metrics: Optional[str | os.PathLike] = None
    output_suggestion: Optional[str | os.PathLike] = None
    demo: bool = False


def run_curriculum(args: CliArgs):
    if not args.demo:
        trainer_state = get_trainer_state(CliArgs.input_trainer_state)
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

    # Outputs
    if not args.mute_trainer_state:
        logger.info(suggestion.model_dump_json())

    if args.output_suggestion is not None:
        with open(Path(args.output_suggestion) / "suggestion.json", "w", encoding="utf-8") as file:
            file.write(suggestion.model_dump_json(indent=2))

    if not args.mute_metrics:
        logger.info(metrics.model_dump_json())

    if args.output_metrics is not None:
        with open(Path(args.output_metrics) / "metrics.json", "w", encoding="utf-8") as file:
            file.write(metrics.model_dump_json(indent=2))


@click.group(name="aind-behavior-curriculum", short_help="AIND Behavior Curriculum CLI")
def main():
    pass


@click.command(short_help="Prints curriculum package version")
def version():
    logger.info(aind_behavior_curriculum_template.__version__)


@click.command(short_help="Prints the aind-behavior-curriculum package version")
def abc_version():
    logger.info(aind_behavior_curriculum.__version__)


@click.command(
    name="run",
    short_help="Runs the curriculum",
    help="Run the curriculum application. A DATA-DIRECTORY and INPUT-TRAINER-STATE inputs are required.",
    no_args_is_help=True,
)
@click.argument("data_directory")
@click.argument("input_trainer_state")
@click.option(
    "--mute-trainer-state",
    default=False,
    help="Mutes the output of the TrainerState suggestion",
    show_default=True,
    is_flag=True,
)
@click.option(
    "--mute-metrics",
    default=False,
    help="Mutes the output of Metrics used to the Trainer",
    show_default=True,
    is_flag=True,
)
@click.option(
    "--output-metrics",
    default=None,
    help="A path to save the used metrics. If not provided, the metrics will not be serialized to a file.",
    show_default=True,
)
@click.option(
    "--output-suggestion",
    default=None,
    help="A path to save the suggestion. If not provided, the suggestion will not be serialized to a file.",
    show_default=True,
)
@click.option(
    "--demo",
    default=False,
    help="Run the curriculum in demo mode. Used for unittest only!",
    show_default=True,
    is_flag=True,
)
def run(**args):
    parsed = CliArgs(**args)
    run_curriculum(parsed)


main.add_command(version)
main.add_command(abc_version)
main.add_command(run)


if __name__ == "__main__":
    main()
