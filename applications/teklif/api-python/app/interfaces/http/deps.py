from collections.abc import Generator

from sqlalchemy.orm import Session

from app.bootstrap.container import Container
from app.infrastructure.db.session import get_db_session


def get_container(session: Session) -> Container:
    return Container(session)


def db_session_dependency() -> Generator[Session, None, None]:
    yield from get_db_session()
