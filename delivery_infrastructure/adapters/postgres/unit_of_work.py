from typing import Optional
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session

from delivery_other.i_unit_of_work import IUnitOfWork


class UnitOfWork(IUnitOfWork, AbstractContextManager):
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session: Optional[Session] = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self.session.close()


    async def __aenter__(self):
        pass


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


    def commit(self) -> bool:
        try:
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def rollback(self):
        self.session.rollback()