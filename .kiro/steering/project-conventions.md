# Project Conventions — PySide6 Desktop App (uv + src layout)

This document describes the standard structure and conventions for PySide6 desktop application projects managed with `uv`.

## Project Structure

```
├── assets/                # App icons, images, static resources
├── src/<package_name>/
│   ├── __init__.py
│   ├── main.py            # Entry point with QMainWindow and viewer classes
│   └── clean.py           # Build artifact cleanup script
├── tests/
│   ├── conftest.py        # pytest-qt session fixtures (qapp)
│   └── test_main.py       # Unit tests
├── app.spec               # PyInstaller build spec
├── pyproject.toml         # Project config, dependencies, scripts, tool settings
└── README.md
```

## Package Manager

- Use `uv` exclusively (not pip, poetry, or pipenv)
- `uv sync` to install dependencies
- `uv run <script>` to execute entry points defined in `[project.scripts]`
- Dev dependencies go in `[dependency-groups] dev = [...]`

## Coding Standards

- **Python version**: 3.12+
- **Type hints**: Required on all functions (mypy strict mode)
- **Linter**: ruff (line-length 88, target py312)
- **Type checker**: mypy (strict = true, ignore_missing_imports = true)
- **Formatter**: ruff format
- For untyped third-party libraries, use `# type: ignore[no-untyped-call]` on the specific line

## PySide6 Viewer Pattern

When adding a new file format viewer:

1. Create a class inheriting from an appropriate Qt widget (QGraphicsView, QPdfView, QTextBrowser, etc.)
2. Implement the standard interface:
   - `zoom_changed = Signal(float)` — emitted when zoom level changes
   - `zoom_in()` / `zoom_out()` / `reset_zoom()` — zoom controls
   - `pan(dx: int, dy: int)` — scroll/pan by pixel offset
   - `keyPressEvent()` — handle PgUp/PgDn for navigation/scrolling
   - `wheelEvent()` — mouse wheel zoom (Ctrl+wheel for text-based viewers)
3. Add the viewer to `MainWindow.stacked_widget`
4. Connect `zoom_changed` signal to `_update_zoom_label`
5. Update `SUPPORTED_EXTENSIONS` tuple and `load_file()` dispatch
6. Update the file dialog filter string

## Key Conventions

- `APP_TITLE` constant for window title (include version)
- `SUPPORTED_EXTENSIONS` tuple as single source of truth for accepted formats
- Status bar for user feedback (loaded file path, errors)
- Unsupported formats show QMessageBox.warning and status bar error
- Drag & Drop support on MainWindow and individual viewers
- Window icon set from `assets/icon.svg`

## Build & Test Commands

```bash
uv sync                      # Install all dependencies
uv run app                   # Run the application
uv run clean                 # Remove build artifacts (preserves dist/svgvvr.exe)
uv run ruff check .          # Lint
uv run mypy src/<pkg>/       # Type check
uv run pytest tests/ -v      # Run tests
uv run pyinstaller app.spec  # Build standalone exe
```

## Testing

- Use `pytest` + `pytest-qt` (import as `pytestqt`)
- Session-scoped `qapp` fixture in `conftest.py`
- Test window initialization, viewer interactions, and error handling
- Import constants (like `APP_TITLE`) from source to avoid hardcoded strings in tests

## PyInstaller (app.spec)

- Entry point: `src/<package_name>/main.py`
- Include `assets/` in `datas` for icons
- Set `icon='assets/icon.ico'` in EXE section
- `console=False` for GUI apps

## Clean Script

- Removes: `build/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `__pycache__/`, `*.pyc`
- Preserves: `app.spec`, `dist/svgvvr.exe`
- Located at `src/<package_name>/clean.py`, registered as `[project.scripts] clean`
