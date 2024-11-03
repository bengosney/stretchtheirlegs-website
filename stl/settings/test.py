import dj_database_url
from testcontainers.postgres import PostgresContainer

from stl.settings.dev import *  # noqa: F403

postgres = PostgresContainer("postgres:14.12-alpine")
postgres.start()

db_url = postgres.get_connection_url().replace("postgresql+psycopg2://", "postgresql://")

DATABASES = {"default": dj_database_url.parse(db_url)}
