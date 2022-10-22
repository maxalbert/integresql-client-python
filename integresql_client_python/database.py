import http.client
from typing import Union, NoReturn

from . import errors
from .dbinfo import DBInfo


class Database:
    def __init__(self, integresql: "IntegreSQL", tpl_hash: str) -> None:
        self.integresql = integresql
        self.tpl_hash = tpl_hash
        self.dbinfo = None

    def open(self) -> DBInfo:
        rsp = self.integresql.request("GET", f"/templates/{self.tpl_hash}/tests")
        if rsp.status_code == http.client.OK:
            return DBInfo(rsp.json())
        elif rsp.status_code == http.client.NOT_FOUND:
            raise errors.TemplateNotFound()
        elif rsp.status_code == http.client.GONE:
            raise errors.DatabaseDiscarded()
        elif rsp.status_code == http.client.SERVICE_UNAVAILABLE:
            raise errors.ManagerNotReady()
        else:
            raise errors.IntegreSQLError(f"Received unexpected HTTP status {rsp.status_code}")

    def mark_unmodified(self, db_id: Union[int, DBInfo]) -> NoReturn:
        if isinstance(db_id, DBInfo):
            db_id = db_id.db_id

        if db_id is None:
            raise errors.IntegreSQLError("Invalid database id")

        rsp = self.integresql.request("DELETE", f"/templates/{self.tpl_hash}/tests/{db_id}")
        if rsp.status_code == http.client.NO_CONTENT:
            return
        elif rsp.status_code == http.client.NOT_FOUND:
            raise errors.TemplateNotFound()
        elif rsp.status_code == http.client.SERVICE_UNAVAILABLE:
            raise errors.ManagerNotReady()
        else:
            raise errors.IntegreSQLError(f"Received unexpected HTTP status {rsp.status_code}")

    def __enter__(self) -> DBInfo:
        self.dbinfo = self.open()
        return self.dbinfo

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa
        pass
