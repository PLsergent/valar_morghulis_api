from invoke import task


@task
def revise(ctx, name):
    ctx.run(f"poetry run alembic revision --autogenerate -m {name}")


@task
def migrate(ctx):
    ctx.run("poetry run alembic upgrade head")


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
def run(ctx):
    ctx.run("poetry run uvicorn app.main:app --reload")


@task
def test(ctx):
    ctx.run("poetry run pytest --color=yes")


@task
def watch(ctx):
    ctx.run("find app -name '*.py' | etr poetry run pytest")
