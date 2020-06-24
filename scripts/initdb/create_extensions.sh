#!/bin/bash
# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
create extension if not exists "uuid-ossp";
EOSQL
