import dj_database_url
import yaml

from stl.settings.dev import *  # noqa: F403

with open(".circleci/config.yml") as file:
    config = yaml.safe_load(file)

jobs = config.get("jobs", {})
build = jobs.get("build", {})
docker = build.get("docker", [])
database_url = None

for docker_image in docker:
    environment = docker_image.get("environment", {})
    if "DATABASE_URL" in environment:
        database_url = environment["DATABASE_URL"]
        break

if database_url:
    DATABASES = {"default": dj_database_url.parse(database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "testdatabase",
        }
    }
