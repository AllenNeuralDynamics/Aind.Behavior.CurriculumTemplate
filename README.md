# Aind.Behavior.CurriculumTemplate

A template of a repository to be used for defining, running and interfacing with a behavior curriculum.

## Getting started

1. Create an environment with `pyproject.toml`. If you have `uv` you can also use the lockfile.
2. Run a curriculum by typing `<path_to_module>/app.py <...>`. To see the available options pass the `-h` flag.
3. The CLI should print out a serialized version of a task suggestion using the `CurriculumCliOutput` model
4. Use the structure of this repository to define your own curriculum. You can define an alias for the CLI command by adding:

    ```toml
    [project.scripts]
    curriculum = "aind_behavior_curriculum_template.app:main"
    ```

    to your `pyproject.toml` file.