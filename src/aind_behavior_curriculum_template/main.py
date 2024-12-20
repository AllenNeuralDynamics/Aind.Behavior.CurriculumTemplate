from __future__ import annotations

import inspect
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import click
import aind_behavior_curriculum
import aind_behavior_curriculum_template

logger = logging.getLogger(__name__)


def run_curriculum(args: _RunCliArgs):
    metric1 = len(str(args.data_directory)) / 10.0

    from aind_behavior_curriculum_template.curriculum import (
        Policy,
        TemplateMetrics,
        p_set_mode_from_metric1,
        s_stage_a,
        trainer,
    )

    test_trainer_state = trainer.create_trainer_state(
        stage=s_stage_a,
        is_on_curriculum=True,
        active_policies=tuple([Policy(rule=x) for x in [p_set_mode_from_metric1]]),
    )

    test_metrics = TemplateMetrics(
        metric1=metric1, metric2_history=[1.0, 2.0, 3.0]
    )  # Changing metric1 will change the suggestion

    suggestion = trainer.evaluate(test_trainer_state, test_metrics)
    print(suggestion.model_dump_json(indent=2))
    logging.info(suggestion.model_dump_json(indent=2))


@click.group(name="aind-behavior-curriculum", short_help="AIND Behavior Curriculum CLI")
def main():
    pass


@click.command(short_help="prints curriculum package version")
def version():
    logger.info(aind_behavior_curriculum_template.__version__)


@click.command(short_help="prints the aind-behavior-curriculum package version")
def abc_version():
    logger.info(aind_behavior_curriculum.__version__)


@click.command(
    name="run",
    short_help="runs the curriculum",
    help="Run the curriculum application. A DATA-DIRECTORY input is required.",
    no_args_is_help=True,
)
@click.argument("data_directory")
@click.option(
    "--skip-upload", default=False, help="Update the suggestions at remote end-point", show_default=True, is_flag=True
)
@click.option(
    "--extras", help="Extra arguments to be passed to the curriculum in the form of 'k1:v1, k2:v2'", default=""
)
def run(data_directory: str | os.PathLike, skip_upload: bool, extras: str):
    parsed = _RunCliArgs(data_directory=Path(data_directory), skip_upload=skip_upload, extras=extras)
    run_curriculum(parsed)


main.add_command(version)
main.add_command(curriculum_version)
main.add_command(run)


@dataclass(frozen=True, slots=True)
class _RunCliArgs:
    data_directory: os.PathLike = field()
    skip_upload: bool = False
    extras: str | dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.extras, str):
            object.__setattr__(self, "extras", self._parse_extra_args(self.extras))

    @staticmethod
    def _parse_extra_args(args: str) -> dict[str, str]:
        extra_kwargs: dict[str, str] = {}
        candidate_args = args.split(",")
        if len(args) == 0:
            return extra_kwargs
        for arg in candidate_args:
            try:
                arg = arg.replace(" ", "")
                key, value = arg.split(":")
                extra_kwargs[key] = value
            except ValueError as e:
                logger.error("Invalid extra argument: %s. Parameters must be in the form of 'k1:v1, k2:v2'", arg)
                raise e
        return extra_kwargs

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{
                cls._sanitize_key(k): v
                for k, v in env.items()
                if cls._sanitize_key(k) in inspect.signature(cls).parameters
            }
        )

    @staticmethod
    def _sanitize_key(key: str) -> str:
        return key.replace("-", "_")


if __name__ == "__main__":
    main()
