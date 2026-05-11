# Png/Svg/Pdf/Markdown Viewer

A lightweight desktop file viewer built with PySide6 (Qt6).  
Supports PNG, JPG, SVG, PDF, and Markdown files in a single window.

## Features

- **Multi-format support** — PNG, JPG, SVG (vector), PDF (vector via QtPdf), Markdown (rendered HTML)
- **High fidelity** — SVG and PDF stay crisp at any zoom level
- **Interactive controls**
  - Zoom: mouse wheel or [+] / [-] buttons
  - Pan: mouse drag or arrow buttons
  - PDF page navigation: Prev/Next buttons, PgUp/PgDn keys
  - Markdown scroll: PgUp/PgDn keys
- **Drag & Drop** — drop any supported file onto the window to open it
- **Load button** — traditional file picker with categorized filters
- **Status bar** — displays the loaded file path or error messages
- **App icon** — custom SVG/ICO icon for the window and built executable

## Supported Formats

| Format | Extensions | Viewer |
|--------|-----------|--------|
| Raster images | `.png`, `.jpg`, `.jpeg` | GraphicsViewer (QGraphicsView) |
| Vector images | `.svg` | GraphicsViewer (QGraphicsSvgItem) |
| PDF documents | `.pdf` | PdfViewer (QPdfView) |
| Markdown | `.md`, `.markdown` | MarkdownViewer (QTextBrowser) |

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

## Getting Started

### Install dependencies

```bash
uv sync
```

### Run the application

```bash
uv run app
```

### Build standalone executable (Windows)

Generates `svgvvr.exe` in the `dist/` directory with the app icon embedded.

```bash
uv run pyinstaller app.spec
```

### Lint & Type Check

```bash
uv run ruff check .
uv run mypy src/my_app/
```

### Run Tests

```bash
uv run pytest tests/ -v
```

### Clean build artifacts

```bash
uv run clean
```

## Project Structure

```
├── assets/
│   ├── icon.svg          # App icon (SVG source)
│   └── icon.ico          # App icon (Windows ICO, multi-size)
├── src/my_app/
│   ├── main.py           # Application entry point & all viewers
│   ├── clean.py          # Build artifact cleanup script
│   └── __init__.py
├── tests/
│   ├── conftest.py       # pytest-qt fixtures
│   └── test_main.py      # Unit tests
├── app.spec              # PyInstaller build spec
├── pyproject.toml        # Project config & dependencies
└── README.md
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| PgDn | PDF: next page / Markdown: scroll down |
| PgUp | PDF: previous page / Markdown: scroll up |
| Ctrl + Mouse Wheel | Markdown: zoom in/out |
| Mouse Wheel | Image/SVG/PDF: zoom in/out |

## License

See [LICENSE](LICENSE) for details.
