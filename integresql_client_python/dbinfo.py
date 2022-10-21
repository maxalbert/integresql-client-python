class DBInfo:
    __slots__ = ('db_id', 'tpl_hash', 'host', 'port', 'user', 'password', 'name')

    def __init__(self, info: dict) -> None:
        self.db_id = info.get('id')
        self.tpl_hash = info['database']['templateHash']

        info = info['database']['config']
        self.host = info['host']
        self.port = info['port']
        self.user = info['username']
        self.password = info['password']
        self.name = info['database']

    def __str__(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    __repr__ = __str__
