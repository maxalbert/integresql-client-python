import os
import sys
from typing import Optional, NoReturn

import requests as requests

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
            base_url = os.environ.get(ENV_INTEGRESQL_CLIENT_BASE_URL, DEFAULT_CLIENT_BASE_URL)
        if not api_version:
            api_version = os.environ.get(ENV_INTEGRESQL_CLIENT_API_VERSION, DEFAULT_CLIENT_API_VERSION)

        self.base_url = base_url
        self.api_version = api_version
        self.debug = False
        self._connection = None

    def template(self, *tpl_dirs, tpl_hash=None):
        if len(tpl_dirs) == 0 and tpl_hash is None:
            raise ValueError("Must provide one or more template directories, or alternatively a value for `tpl_hash`.")
        elif len(tpl_dirs) >= 1 and tpl_hash is not None:
            raise ValueError("Template directories cannot be combined with argument `tpl_hash`")
        elif tpl_hash is not None:
            return TemplateCtx(integresql=self, tpl_hash=tpl_hash)
        else:
            return TemplateCtx.from_template_dirs(integresql=self, tpl_dirs=tpl_dirs)

    @property
    def connection(self) -> requests.Session:
        if not self._connection:
            self._connection = requests.Session()

        return self._connection

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: Optional[dict] = None,
    ) -> requests.Response:
        path = path.lstrip("/")
        url = f"{self.base_url}/{self.api_version}/{path}"

        if self.debug:
            print(f"Request {method.upper()} to {url} with data {payload}", file=sys.stderr)

        rsp = self.connection.request(method, url, data=payload)

        if self.debug:
            print(f"Response from {method.upper()} {url}: [{rsp.status_code}] {rsp.content}", file=sys.stderr)

        return rsp

    def close(self) -> NoReturn:
        # self._tpl_hash = None
        if self._connection:
            self._connection.close()
            self._connection = None
