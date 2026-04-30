from typing import Generator
import pytest
from PySide6.QtWidgets import QApplication
import sys

@pytest.fixture(scope="session")
def qapp() -> Generator[QApplication, None, None]:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    if not isinstance(app, QApplication):
        raise TypeError("Existing instance is not a QApplication")
    yield app
