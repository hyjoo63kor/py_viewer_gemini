from pathlib import Path
from PySide6.QtWidgets import QApplication
from pytest_qt.qtbot import QtBot
from my_app.main import MainWindow

def test_main_window_init(qtbot: QtBot, qapp: QApplication) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "Png/Svg/Pdf Viewer"

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
    
    # Should not crash on unsupported files (or should we add handling?)
    p = Path("non_existent.xyz")
    window.load_file(p)
    assert window.windowTitle() == f"Png/Svg/Pdf Viewer - {p.name}"
