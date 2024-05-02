from pathlib import Path
from tempfile import gettempdir


class NicePath(str):
    """Render a prettier version of the path."""
    def __new__(cls, path):
        string = str(path.absolute())

        if Path.cwd() in path.parents:
            return string.replace(str(Path.cwd()), '.')

        elif Path.home() in path.parents:
            return string.replace(str(Path.home()), '~')

        temp_path = Path(gettempdir()).resolve()
        if temp_path in path.parents:
            return string.replace(str(temp_path), '$TMPDIR')

        return string



