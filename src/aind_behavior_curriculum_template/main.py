import inspect
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import click

from aind_behavior_curriculum_template import __version__
from aind_behavior_curriculum_template import __version__ as aind_behavior_curriculum_template_version

logger = logging.getLogger(__name__)


def run_curriculum(args):
    args = vars(args)
    parsed = _RunCliArgs.from_dict(args)


@click.group(name="aind-behavior-curriculum", short_help="AIND Behavior Curriculum CLI")
def main():
    pass


@click.command(short_help="prints curriculum version")
def version():
    logger.info(__version__)


@click.command(short_help="prints aind-behavior-curriculum version")
def version_aind_behavior_curriculum_template():
    logger.info(aind_behavior_curriculum_template_version)


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


main.add_command(version)
main.add_command(version_aind_behavior_curriculum_template)
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
