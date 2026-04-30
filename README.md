# Png/Svg/Pdf Viewer (svgvvr)

A versatile desktop application built with PySide6 to view PNG, JPG, SVG, and PDF files with high fidelity.

## Features
- **Multi-format Support**: PNG, JPG, SVG (vector), and PDF (vector via QtPdf).
- **High Fidelity**: SVG and PDF maintain crispness at any zoom level.
- **Interactive Controls**:
  - **Zoom**: Mouse wheel or [+][-] buttons.
  - **Pan**: Mouse left-drag or arrow buttons.
  - **Navigation**: Prev/Next buttons for PDF pages.
- **Drag & Drop**: Easily load files by dragging them into the window.
- **Load Button**: Traditional file picker support.

## Development

### Setup
Ensure you have [uv](https://github.com/astral-sh/uv) installed.
```bash
uv sync
```

### Run
```bash
uv run py-viewer
```

### Build (Windows)
Generates a standalone `svgvvr.exe` in the `dist/` directory.
```bash
uv run pyinstaller app.spec
```

### Test & Lint
```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

### Clean
Removes build artifacts and cache folders.
```bash
uv run clean
```
