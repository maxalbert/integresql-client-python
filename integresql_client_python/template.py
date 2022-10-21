import http.client

from . import errors
from .dbinfo import DBInfo
from typing import Optional, NoReturn, Union, List


class Template:
    def __init__(self, *, integresql, tpl_hash):
        self.integresql = integresql
        self.tpl_hash = tpl_hash
        self.dbinfo = None

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

    def finalize(self) -> NoReturn:
        rsp = self.integresql.request("PUT", f"/templates/{self.tpl_hash}")
        if rsp.status_code == http.client.NO_CONTENT:
            return
        elif rsp.status_code == http.client.NOT_FOUND:
            raise errors.TemplateNotFound()
        elif rsp.status_code == http.client.SERVICE_UNAVAILABLE:
            raise errors.ManagerNotReady()
        else:
            raise errors.IntegreSQLError(f"Received unexpected HTTP status {rsp.status_code}")

    def __enter__(self) -> DBInfo:
        return self.dbinfo

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa
        self.finalize()
        # print(f"[DDD] TODO: implement self.finalize() and call it from here")


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
