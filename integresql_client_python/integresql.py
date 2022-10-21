import os
from typing import Optional

ENV_INTEGRESQL_CLIENT_BASE_URL = "INTEGRESQL_CLIENT_BASE_URL"
ENV_INTEGRESQL_CLIENT_API_VERSION = "INTEGRESQL_CLIENT_API_VERSION"
DEFAULT_CLIENT_BASE_URL = "http://integresql:5000/api"  # noqa
DEFAULT_CLIENT_API_VERSION = "v1"

from .template import TemplateCtx


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
        return TemplateCtx(integresql=self, tpl_hash=tpl_hash)
