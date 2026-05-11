import sys
from pathlib import Path
from typing import Optional, Union, cast

import markdown
from PySide6.QtCore import Qt, Signal, Slot, QPointF, QPoint
from PySide6.QtGui import (
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QIcon,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPixmap,
    QResizeEvent,
    QWheelEvent,
)
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
    QFrame,
    QStackedWidget,
)

SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".svg", ".pdf", ".md", ".markdown")
APP_TITLE = "Png/Svg/Pdf/Markdown Viewer ver.0.2.0"
_ICON_DIR = Path(__file__).parent.parent.parent / "assets"


class GraphicsViewer(QGraphicsView):
    zoom_changed = Signal(float)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Panning logic: We'll use ScrollHandDrag for native-like feel
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self._zoom_factor = 1.0
        self._pixmap_item: Optional[QGraphicsPixmapItem] = None
        self._svg_item: Optional[QGraphicsSvgItem] = None

    def clear_view(self) -> None:
        self._scene.clear()
        self._pixmap_item = None
        self._svg_item = None
        self._zoom_factor = 1.0
        self.resetTransform()
        self.zoom_changed.emit(self._zoom_factor)

    def load_image(self, file_path: Path) -> None:
        self.clear_view()
        pixmap = QPixmap(str(file_path))
        if not pixmap.isNull():
            self._pixmap_item = QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._pixmap_item)
            self._scene.setSceneRect(self._pixmap_item.boundingRect())
            self.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
            self._update_zoom_from_transform()

    def load_svg(self, file_path: Path) -> None:
        self.clear_view()
        self._svg_item = QGraphicsSvgItem(str(file_path))
        self._scene.addItem(self._svg_item)
        self._scene.setSceneRect(self._svg_item.boundingRect())
        self.fitInView(self._svg_item, Qt.AspectRatioMode.KeepAspectRatio)
        self._update_zoom_from_transform()

    def _update_zoom_from_transform(self) -> None:
        self._zoom_factor = self.transform().m11()
        self.zoom_changed.emit(self._zoom_factor)

    def zoom_in(self) -> None:
        self._apply_zoom(1.2)

    def zoom_out(self) -> None:
        self._apply_zoom(1 / 1.2)

    def reset_zoom(self) -> None:
        self.resetTransform()
        if self._pixmap_item:
            self.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        elif self._svg_item:
            self.fitInView(self._svg_item, Qt.AspectRatioMode.KeepAspectRatio)
        self._update_zoom_from_transform()

    def _apply_zoom(self, factor: float) -> None:
        self.scale(factor, factor)
        self._update_zoom_from_transform()

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def pan(self, dx: int, dy: int) -> None:
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + dx)
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() + dy)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            file_path = Path(urls[0].toLocalFile())
            window = self.window()
            if isinstance(window, MainWindow):
                window.load_file(file_path)


class PdfViewer(QPdfView):
    zoom_changed = Signal(float)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent if parent else cast(QWidget, None))
        self.setPageMode(QPdfView.PageMode.SinglePage)
        self.setZoomMode(QPdfView.ZoomMode.FitInView)

        self._document = QPdfDocument(self)
        self.setDocument(self._document)

        self._zoom_factor = 1.0
        self._updating_zoom = False

        # Panning state for QPdfView
        self._is_panning = False
        self._last_mouse_pos = QPoint()

    def load_pdf(self, file_path: Path) -> None:
        self._document.load(str(file_path))
        self.setZoomMode(QPdfView.ZoomMode.FitInView)
        self._update_zoom_factor()

    def _update_zoom_factor(self) -> None:
        if self._updating_zoom:
            return
        self._updating_zoom = True
        new_factor = self.zoomFactor()
        if new_factor != self._zoom_factor:
            self._zoom_factor = new_factor
            self.zoom_changed.emit(self._zoom_factor)
        self._updating_zoom = False

    def zoom_in(self) -> None:
        self.setZoomMode(QPdfView.ZoomMode.Custom)
        self.setZoomFactor(self.zoomFactor() * 1.2)
        self._update_zoom_factor()

    def zoom_out(self) -> None:
        self.setZoomMode(QPdfView.ZoomMode.Custom)
        self.setZoomFactor(self.zoomFactor() / 1.2)
        self._update_zoom_factor()

    def reset_zoom(self) -> None:
        self.setZoomMode(QPdfView.ZoomMode.FitInView)
        self._update_zoom_factor()

    def next_page(self) -> None:
        nav = self.pageNavigator()
        if nav and nav.currentPage() < self._document.pageCount() - 1:
            nav.jump(nav.currentPage() + 1, QPointF(0, 0), nav.currentZoom())

    def prev_page(self) -> None:
        nav = self.pageNavigator()
        if nav and nav.currentPage() > 0:
            nav.jump(nav.currentPage() - 1, QPointF(0, 0), nav.currentZoom())

    def pan(self, dx: int, dy: int) -> None:
        h_bar = self.horizontalScrollBar()
        v_bar = self.verticalScrollBar()
        h_bar.setValue(h_bar.value() + dx)
        v_bar.setValue(v_bar.value() + dy)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    # Panning implementation for QPdfView
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_panning = True
            self._last_mouse_pos = event.pos()
            self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_panning:
            delta = event.pos() - self._last_mouse_pos
            self._last_mouse_pos = event.pos()
            h_bar = self.horizontalScrollBar()
            v_bar = self.verticalScrollBar()
            h_bar.setValue(h_bar.value() - delta.x())
            v_bar.setValue(v_bar.value() - delta.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_panning = False
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        # Cancel any panning state during window resize to prevent freeze
        self._is_panning = False
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        super().resizeEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_PageDown:
            self.next_page()
            event.accept()
        elif key == Qt.Key.Key_PageUp:
            self.prev_page()
            event.accept()
        else:
            super().keyPressEvent(event)


_MARKDOWN_CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    color: #24292e;
    padding: 20px 32px;
    max-width: 900px;
    margin: 0 auto;
}
h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}
h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
h3 { font-size: 1.25em; }
code {
    background-color: #f6f8fa;
    border-radius: 3px;
    padding: 0.2em 0.4em;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 85%;
}
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    line-height: 1.45;
}
pre code {
    background-color: transparent;
    padding: 0;
}
blockquote {
    border-left: 4px solid #dfe2e5;
    color: #6a737d;
    padding: 0 16px;
    margin: 0 0 16px 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 16px;
}
th, td {
    border: 1px solid #dfe2e5;
    padding: 6px 13px;
}
th { background-color: #f6f8fa; font-weight: 600; }
a { color: #0366d6; text-decoration: none; }
a:hover { text-decoration: underline; }
ul, ol { padding-left: 2em; }
hr { border: none; border-top: 1px solid #eaecef; margin: 24px 0; }
img { max-width: 100%; }
"""


class MarkdownViewer(QTextBrowser):
    """Renders Markdown files as styled HTML using QTextBrowser."""

    zoom_changed = Signal(float)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setOpenExternalLinks(True)
        self.setReadOnly(True)

        self._zoom_factor = 1.0
        self._base_font_size = 15
        self._md_converter = markdown.Markdown(  # type: ignore[no-untyped-call]
            extensions=["tables", "fenced_code", "codehilite", "toc", "nl2br"],
            extension_configs={"codehilite": {"guess_lang": False, "css_class": "code"}},
        )
        self._file_path: Optional[Path] = None

    def load_markdown(self, file_path: Path) -> None:
        self._file_path = file_path
        self._md_converter.reset()
        text = file_path.read_text(encoding="utf-8")
        html_body = self._md_converter.convert(text)
        full_html = (
            f"<html><head><style>{_MARKDOWN_CSS}</style></head>"
            f"<body>{html_body}</body></html>"
        )
        # Set search path so relative images resolve correctly
        self.setSearchPaths([str(file_path.parent)])
        self.setHtml(full_html)
        self._zoom_factor = 1.0
        self.zoom_changed.emit(self._zoom_factor)

    def zoom_in(self) -> None:
        self._apply_zoom(1.2)

    def zoom_out(self) -> None:
        self._apply_zoom(1 / 1.2)

    def reset_zoom(self) -> None:
        self._zoom_factor = 1.0
        font = self.font()
        font.setPointSize(self._base_font_size)
        self.setFont(font)
        self.zoom_changed.emit(self._zoom_factor)

    def _apply_zoom(self, factor: float) -> None:
        self._zoom_factor *= factor
        new_size = max(6, int(self._base_font_size * self._zoom_factor))
        font = self.font()
        font.setPointSize(new_size)
        self.setFont(font)
        self.zoom_changed.emit(self._zoom_factor)

    def pan(self, dx: int, dy: int) -> None:
        h_bar = self.horizontalScrollBar()
        v_bar = self.verticalScrollBar()
        h_bar.setValue(h_bar.value() + dx)
        v_bar.setValue(v_bar.value() + dy)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_PageDown:
            self.pan(0, 300)
            event.accept()
        elif key == Qt.Key.Key_PageUp:
            self.pan(0, -300)
            event.accept()
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1000, 800)
        self.setAcceptDrops(True)

        # Window icon
        icon_path = _ICON_DIR / "icon.svg"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Viewers
        self.stacked_widget = QStackedWidget()
        self.graphics_viewer = GraphicsViewer()
        self.pdf_viewer = PdfViewer()
        self.markdown_viewer = MarkdownViewer()

        self.stacked_widget.addWidget(self.graphics_viewer)
        self.stacked_widget.addWidget(self.pdf_viewer)
        self.stacked_widget.addWidget(self.markdown_viewer)

        self.graphics_viewer.zoom_changed.connect(self._update_zoom_label)
        self.pdf_viewer.zoom_changed.connect(self._update_zoom_label)
        self.markdown_viewer.zoom_changed.connect(self._update_zoom_label)

        # UI Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_panel = QFrame()
        top_panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        top_layout = QVBoxLayout(top_panel)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(4)

        instructions = QLabel(
            "[Load] or Drag & Drop | Mouse Wheel: Zoom | Mouse Drag: Pan | PgUp/PgDn: Page/Scroll"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(instructions)

        controls_layout = QHBoxLayout()

        btn_load = QPushButton("📂 Load File")
        btn_load.clicked.connect(self._open_file_dialog)
        controls_layout.addWidget(btn_load)

        controls_layout.addSpacing(20)

        self.btn_prev = QPushButton("◀ Prev Page")
        self.btn_next = QPushButton("Next Page ▶")
        self.btn_prev.clicked.connect(self.pdf_viewer.prev_page)
        self.btn_next.clicked.connect(self.pdf_viewer.next_page)
        self.btn_prev.setEnabled(False)
        self.btn_next.setEnabled(False)

        controls_layout.addWidget(self.btn_prev)
        controls_layout.addWidget(self.btn_next)

        controls_layout.addStretch()

        btn_zoom_out = QPushButton("[-]")
        btn_zoom_in = QPushButton("[+]")
        btn_reset = QPushButton("Reset")
        self.zoom_label = QLabel("Zoom: 100%")

        btn_zoom_out.clicked.connect(self._zoom_out)
        btn_zoom_in.clicked.connect(self._zoom_in)
        btn_reset.clicked.connect(self._reset_zoom)

        controls_layout.addWidget(btn_zoom_out)
        controls_layout.addWidget(self.zoom_label)
        controls_layout.addWidget(btn_zoom_in)
        controls_layout.addWidget(btn_reset)

        controls_layout.addStretch()

        btn_left = QPushButton("←")
        btn_up = QPushButton("↑")
        btn_down = QPushButton("↓")
        btn_right = QPushButton("→")

        btn_up.clicked.connect(lambda: self._pan(0, -50))
        btn_down.clicked.connect(lambda: self._pan(0, 50))
        btn_left.clicked.connect(lambda: self._pan(-50, 0))
        btn_right.clicked.connect(lambda: self._pan(50, 0))

        controls_layout.addWidget(btn_left)
        controls_layout.addWidget(btn_up)
        controls_layout.addWidget(btn_down)
        controls_layout.addWidget(btn_right)

        top_layout.addLayout(controls_layout)
        main_layout.addWidget(top_panel)
        main_layout.addWidget(self.stacked_widget)

        # Status bar
        self._status_bar = self.statusBar()
        self._status_bar.showMessage("Ready")

    def _current_viewer(self) -> Union[GraphicsViewer, PdfViewer, MarkdownViewer]:
        widget = self.stacked_widget.currentWidget()
        if isinstance(widget, (GraphicsViewer, PdfViewer, MarkdownViewer)):
            return widget
        raise RuntimeError("Unexpected widget in stacked widget")

    def _zoom_in(self) -> None:
        self._current_viewer().zoom_in()

    def _zoom_out(self) -> None:
        self._current_viewer().zoom_out()

    def _reset_zoom(self) -> None:
        self._current_viewer().reset_zoom()

    def _pan(self, dx: int, dy: int) -> None:
        self._current_viewer().pan(dx, dy)

    def _open_file_dialog(self) -> None:
        file_path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            (
                "Supported Files (*.png *.jpg *.jpeg *.svg *.pdf *.md *.markdown);;"
                "Images (*.png *.jpg *.jpeg *.svg);;"
                "PDF (*.pdf);;"
                "Markdown (*.md *.markdown);;"
                "All Files (*)"
            ),
        )
        if file_path_str:
            self.load_file(Path(file_path_str))

    def load_file(self, file_path: Path) -> None:
        suffix = file_path.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            msg = (
                f"'{suffix}' is not a supported file format. "
                f"Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
            )
            QMessageBox.warning(self, "Unsupported Format", msg)
            self._status_bar.showMessage(f"Error: {msg}")
            return

        if suffix in (".png", ".jpg", ".jpeg"):
            self.stacked_widget.setCurrentWidget(self.graphics_viewer)
            self.graphics_viewer.load_image(file_path)
        elif suffix == ".svg":
            self.stacked_widget.setCurrentWidget(self.graphics_viewer)
            self.graphics_viewer.load_svg(file_path)
        elif suffix == ".pdf":
            self.stacked_widget.setCurrentWidget(self.pdf_viewer)
            self.pdf_viewer.load_pdf(file_path)
        elif suffix in (".md", ".markdown"):
            self.stacked_widget.setCurrentWidget(self.markdown_viewer)
            self.markdown_viewer.load_markdown(file_path)

        self._update_ui_for_file(file_path)
        self._status_bar.showMessage(f"Loaded: {file_path}")

    @Slot(float)
    def _update_zoom_label(self, factor: float) -> None:
        self.zoom_label.setText(f"Zoom: {int(factor * 100)}%")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            file_path = Path(urls[0].toLocalFile())
            self.load_file(file_path)

    def _update_ui_for_file(self, file_path: Path) -> None:
        is_pdf = file_path.suffix.lower() == ".pdf"
        self.btn_prev.setEnabled(is_pdf)
        self.btn_next.setEnabled(is_pdf)
        self.setWindowTitle(f"{APP_TITLE} - {file_path.name}")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_PageDown:
            current = self.stacked_widget.currentWidget()
            if isinstance(current, PdfViewer):
                self.pdf_viewer.next_page()
            elif isinstance(current, MarkdownViewer):
                self.markdown_viewer.pan(0, 300)
            event.accept()
        elif key == Qt.Key.Key_PageUp:
            current = self.stacked_widget.currentWidget()
            if isinstance(current, PdfViewer):
                self.pdf_viewer.prev_page()
            elif isinstance(current, MarkdownViewer):
                self.markdown_viewer.pan(0, -300)
            event.accept()
        else:
            super().keyPressEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
