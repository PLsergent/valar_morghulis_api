#! /usr/bin/env bash
set -e;

# Let the DB start
sleep 5;

# Run migrations
poetry run alembic upgrade head
