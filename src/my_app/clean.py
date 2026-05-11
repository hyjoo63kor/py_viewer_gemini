import shutil
from pathlib import Path

def clean() -> None:
    """Remove build artifacts and cache directories."""
    # Find project root (where pyproject.toml usually lives)
    # Since this script is in src/my_app/clean.py, project root is 2 levels up.
    project_root = Path(__file__).parent.parent.parent.resolve()
    print(f"Project root identified as: {project_root}")
    
    # List of directory names or patterns to remove at root
    dir_targets = [
        "build",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
    ]
    
    # 1. Remove specific directories at root
    for target in dir_targets:
        path = project_root / target
        if path.exists() and path.is_dir():
            print(f"Removing directory: {path}")
            shutil.rmtree(path, ignore_errors=True)

    # 2. Clean dist/ but preserve dist/svgvvr.exe
    dist_dir = project_root / "dist"
    preserve_file = dist_dir / "svgvvr.exe"
    if dist_dir.exists() and dist_dir.is_dir():
        for item in dist_dir.iterdir():
            if item == preserve_file:
                print(f"Preserving: {item}")
                continue
            if item.is_dir():
                print(f"Removing directory: {item}")
                shutil.rmtree(item, ignore_errors=True)
            else:
                print(f"Removing file: {item}")
                item.unlink(missing_ok=True)

    # 3. Remove recursive patterns like __pycache__
    for pycache in project_root.rglob("__pycache__"):
        print(f"Removing recursive __pycache__: {pycache}")
        shutil.rmtree(pycache, ignore_errors=True)

    # 4. Remove recursive file patterns (like .pyc)
    for pyc in project_root.rglob("*.pyc"):
        print(f"Removing file: {pyc}")
        pyc.unlink(missing_ok=True)

    # 5. Handle files at root specifically if needed
    # We skip app.spec to preserve it as requested previously (implicit in usage)
    for spec in project_root.glob("*.spec"):
        if spec.name == "app.spec":
            continue
        print(f"Removing file: {spec}")
        spec.unlink(missing_ok=True)

    print("Clean completed successfully.")

if __name__ == "__main__":
    clean()
