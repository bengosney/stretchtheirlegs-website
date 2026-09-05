import os

import dj_database_url
from testcontainers.community.postgres import PostgresContainer

from stl.settings.dev import *  # noqa: F403

if not (database_url := os.environ.get("DATABASE_URL")):
    postgres = PostgresContainer("postgres:17-alpine")
    postgres.start()
    database_url = postgres.get_connection_url().replace("postgresql+psycopg2://", "postgresql://")

DATABASES = {"default": dj_database_url.parse(database_url)}
