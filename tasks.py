from invoke import task


@task
def up(ctx):
    ctx.run("docker-compose up -d")


@task
def down(ctx):
    ctx.run("docker-compose down")


@task
def build(ctx):
    ctx.run("docker-compose build")


@task
def revise(ctx, name):
    ctx.run(f"poetry run alembic revision --autogenerate -m {name}")


@task
def migrate(ctx):
    ctx.run("poetry run alembic upgrade head")


@task
def run(ctx):
    ctx.run("poetry run uvicorn app.main:app --reload")


@task
def test(ctx):
    ctx.run("poetry run pytest --color=yes --cov")


@task
def watch(ctx):
    ctx.run("find app -name '*.py' | entr poetry run pytest")


@task
def lint(ctx):
    ctx.run("poetry run flake8 app", pty=True)
    ctx.run("poetry run mypy app", pty=True)
    ctx.run("poetry run black --check app", pty=True)
    ctx.run("poetry run isort -c --recursive app", pty=True)


@task
def format(ctx):
    ctx.run("poetry run isort -y --atomic --recursive app", pty=True)
    ctx.run("poetry run autoflake -ri --exclude=__init__.py app", pty=True)
    ctx.run("poetry run black app", pty=True)
