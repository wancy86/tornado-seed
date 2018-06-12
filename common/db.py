from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config


class DB:
    _engine = None

    def __init__(self, dialect='mysql', driver='', user='', password='', host='', database='', TEST=False):
        self.dialect = dialect
        self.driver = driver
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.TEST = TEST
        self._session = None

    @property
    def conn(self):
        self.database = self.database + '_test' if self.TEST else self.database
        connection = '{}+{}://{}:{}@{}/{}?charset=utf8'.format(self.dialect, self.driver, self.user, self.password,
                                                               self.host, self.database)
        return connection

    @property
    def engine(self):
        if not DB._engine:
            DB._engine = create_engine(self.conn, echo=config.ECHO, pool_size=5, pool_recycle=7200)
        return DB._engine

    @property
    def session(self):
        if not self._session:
            self._session = sessionmaker(bind=self.engine, expire_on_commit=False)()
        return self._session

    def close(self):
        if self._session:
            self.session.close()