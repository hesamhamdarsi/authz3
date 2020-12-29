from sys import exit

import click

from authz import app_cli, db

status = True


@app_cli.command("test", help="Testing Application backing connections")
def app_cli_test():
    click.secho("FULL test", bold=True, fg="green")
    if test_database() == True:
        status = True
    else:
        status = False
    ### second test ###
    # if test_redis() == 0
    # ...

    return status
    if status == True:
        exit(0)
    else:
        exit(1)


def test_database():
    click.echo(
        "Testing database connection....", nl=False
    )  # nl=flase means "no new line"
    try:
        result = db.engine.execute("SELECT 1;").first()
        if result[0] == 1:
            click.secho("SUCCESS", bold=True, fg="green")
            return True
        else:
            click.secho("WARNING", bold=True, fg="yellow")
            return False
    except:
        click.secho("FAILED", bold=True, fg="red")
        return False
