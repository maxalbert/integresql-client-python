import os
from typing import Optional

ENV_INTEGRESQL_CLIENT_BASE_URL = "INTEGRESQL_CLIENT_BASE_URL"
ENV_INTEGRESQL_CLIENT_API_VERSION = "INTEGRESQL_CLIENT_API_VERSION"
DEFAULT_CLIENT_BASE_URL = "http://integresql:5000/api"  # noqa
DEFAULT_CLIENT_API_VERSION = "v1"


class Template:
    def __init__(self, tpl_hash):
        self.tpl_hash = tpl_hash

    def __repr__(self):
        return f"<Template: tpl_hash={self.tpl_hash!r}>"


class TemplateCtx:
    def __init__(self, tpl_hash):
        self.tpl_hash = tpl_hash

    @classmethod
    def from_template_dirs(cls, tpl_dirs):
        assert isinstance(tpl_dirs, (list, tuple))
        raise NotImplementedError("TODO: calculate tpl_hash from contents of tpl_dirs")

    def __enter__(self):
        print("[DDD] Entering TemplateCtx context manager")
        return Template(self.tpl_hash)

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa
        print("[DDD] Exiting from TemplateCtx context manager")
        pass


class IntegreSQL:
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
    ) -> None:
        if not base_url:
            base_url = os.environ.get(
                ENV_INTEGRESQL_CLIENT_BASE_URL, DEFAULT_CLIENT_BASE_URL
            )
        if not api_version:
            api_version = os.environ.get(
                ENV_INTEGRESQL_CLIENT_API_VERSION, DEFAULT_CLIENT_API_VERSION
            )

        self.base_url = base_url
        self.api_version = api_version
        self.debug = False
        self._connection = None

    def template(self, tpl_hash):
        return TemplateCtx(tpl_hash=tpl_hash)
