from pathlib import Path
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot
from my_app.main import MainWindow, APP_TITLE

def test_main_window_init(qtbot: QtBot, qapp: QApplication) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == APP_TITLE

def test_viewer_zoom(qtbot: QtBot, qapp: QApplication) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Testing GraphicsViewer zoom (default)
    viewer = window.graphics_viewer
    initial_zoom = viewer._zoom_factor
    viewer.zoom_in()
    assert viewer._zoom_factor > initial_zoom
    
    viewer.zoom_out()
    assert abs(viewer._zoom_factor - initial_zoom) < 0.001
    
    viewer.reset_zoom()
    assert "Zoom:" in window.zoom_label.text()

def test_file_load_unsupported(qtbot: QtBot, qapp: QApplication) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    # Unsupported extension should not change the window title
    p = Path("non_existent.xyz")
    window.load_file(p)
    assert window.windowTitle() == APP_TITLE

def test_status_bar_message(qtbot: QtBot, qapp: QApplication) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    assert window._status_bar.currentMessage() == "Ready"

    # Unsupported file shows error in status bar
    p = Path("test.xyz")
    window.load_file(p)
    assert "Error:" in window._status_bar.currentMessage()
