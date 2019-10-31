import pytest
from testfixtures import LogCapture


@pytest.fixture(autouse=True)
def capture():
    with LogCapture() as capture:
        yield capture
