# Aind.Behavior.CurriculumTemplate
A template of a repository to be used for defining, running and interfacing with a behavior curriculum

## Getting started

1. Create an environment with `pyproject.toml`. If you have `uv` you can also use the lockfile.
2. Run a curriculum by typing `curriculum run <path_to_data>`. The demo is currently ignoring the path to the data and using it instead to change the recommend stage, by calculating a metric based on the length of the path.
3. The CLI should print out a serialized version of a task suggestion.
