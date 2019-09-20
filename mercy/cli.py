# -*- coding: utf-8 -*-

"""Console script for mercy."""
import sys
import click


@click.data()
def main(args=None):
    """Console script for mercy."""
    click.echo("Replace this message by putting your code into "
               "mercy.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
