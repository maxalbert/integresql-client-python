import hashlib
import pathlib
from typing import Union, List


class TemplateDirHash:
    BUFFER_SIZE = 4 * 1024

    def __init__(self, template: Union[str, List[str], pathlib.PurePath, List[pathlib.PurePath], None]) -> None:
        if not isinstance(template, (list, tuple)):
            template = [template]
        self.templates = template

        mhash = hashlib.md5()
        for template in self.templates:
            if not isinstance(template, pathlib.PurePath):
                template = pathlib.Path(template)

            if not template.exists():
                raise RuntimeError(f"Path {template} doesn't exists")

            if not template.is_dir():
                raise RuntimeError(f"Path {template} must be a directory")

            hashed = self.calculate(template)
            mhash.update(hashed.encode())

        self.hash = mhash.hexdigest()

    def __str__(self) -> str:
        return self.hash

    @classmethod
    def calculate(cls, path: pathlib.Path) -> str:
        template_hash = hashlib.md5()  # noqa: S303  # nosec
        items = list(path.rglob('*'))
        items.sort()
        for item in items:
            if item.is_dir():
                continue

            item_hash = hashlib.md5()  # noqa: S303  # nosec
            with item.open('rb') as fh:
                while True:
                    data = fh.read(cls.BUFFER_SIZE)
                    item_hash.update(data)
                    if len(data) < cls.BUFFER_SIZE:
                        break
            template_hash.update(item_hash.hexdigest().encode())

        return template_hash.hexdigest()
