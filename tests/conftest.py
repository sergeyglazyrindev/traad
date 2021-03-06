import logging
import os
import pytest
import shutil
from traad.rope.project import Project
from traad.state import State

from paths import ACTIVE_DIR, PACKAGES_DIR

# We don't want to see logging output for the most part. We intentionally
# trigger cases where traad will log to error, and those just mess up the
# output.
logging.basicConfig(level=logging.CRITICAL)


@pytest.fixture
def start_project():
    projects = []

    def f(main, *cross):
        proj = Project.start(
            os.path.join(ACTIVE_DIR, main),
            cross_project_dirs=[
                os.path.join(ACTIVE_DIR, project)
                for project in cross]).proxy()
        projects.append(proj)
        return proj

    yield f

    for proj in projects:
        proj.stop()


@pytest.fixture
def state():
    state = State.start().proxy()
    try:
        yield state
    finally:
        state.stop()


@pytest.fixture
def activate_package():
    def f(package, into):
        dest_dir = os.path.join(ACTIVE_DIR, into)

        shutil.rmtree(dest_dir, ignore_errors=True)
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass

        shutil.copytree(
            os.path.join(PACKAGES_DIR, package),
            os.path.join(dest_dir, package))

    try:
        yield f
    except:
        pass

    try:
        shutil.rmtree(ACTIVE_DIR)
    except OSError:
        pass
