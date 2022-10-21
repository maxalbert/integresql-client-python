import http.client

from . import errors
from .dbinfo import DBInfo
from typing import Optional, NoReturn, Union, List


class Template:
    def __init__(self, *, integresql, tpl_hash):
        self.integresql = integresql
        self.tpl_hash = tpl_hash

    def __repr__(self):
        return f"<Template: tpl_hash={self.tpl_hash!r}>"

    def initialize(self) -> "Template":
        rsp = self.integresql.request(
            "POST",
            "/templates",
            payload={"hash": str(self.tpl_hash)},
        )
        if rsp.status_code == http.client.OK:
            self.dbinfo = DBInfo(rsp.json())
            return self
        elif rsp.status_code == http.client.LOCKED:
            return self

        if rsp.status_code == http.client.SERVICE_UNAVAILABLE:
            raise errors.ManagerNotReady()
        else:
            raise errors.IntegreSQLError(f"Received unexpected HTTP status {rsp.status_code}")

    def close(self) -> NoReturn:
        self._tpl_hash = None
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> "Template":
        return self.get_template()

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:  # noqa
        self.close()


class TemplateCtx:
    def __init__(self, *, integresql, tpl_hash):
        self.integresql = integresql
        self.tpl_hash = tpl_hash

    @classmethod
    def from_template_dirs(cls, tpl_dirs):
        assert isinstance(tpl_dirs, (list, tuple))
        raise NotImplementedError("TODO: calculate tpl_hash from contents of tpl_dirs")

    def __enter__(self):
        print("[DDD] Entering TemplateCtx context manager")
        return Template(integresql=self.integresql, tpl_hash=self.tpl_hash)

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa
        print("[DDD] Exiting from TemplateCtx context manager")
        pass
