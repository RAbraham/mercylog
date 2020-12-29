import os
from invoke import task

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))


@task
def build(c):
    commands = [
        "jb build book"
    ]
    run_commands(c, commands)

@task
def publish(c):
    commands = [
        "ghp-import -n -p -f book/_build/html"
    ]
    run_commands(c, commands)

    
def run_commands(c, commands):
    for command in commands:
        c.run_df(command)

    