from pathlib import Path

def check_path(path: Path) -> None:
    """Check path if it exists and create it if it doesn't
    Args:
        path (Path): path to check
    Returns:
        None
    """
    if not Path.exists(path):
        Path.mkdir(path)
