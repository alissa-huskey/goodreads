from pathlib import Path
import pytest


@pytest.fixture
def rootdir():
    return Path(__file__).parent.parent


@pytest.fixture
def datadir(rootdir):
    return rootdir / "data"
