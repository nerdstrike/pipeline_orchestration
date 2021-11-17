import pytest
import sqlalchemy
import sqlalchemy.orm
import tempfile

import pipeline_orchestrator.tracking.schema


@pytest.fixture
def sync_session():
    db_file = tempfile.NamedTemporaryFile()
    sqlite_url = 'sqlite:///{}'.format(db_file.name)

    engine = sqlalchemy.create_engine(sqlite_url)
    pipeline_orchestrator.tracking.schema.Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    sess = sqlalchemy.orm.scoped_session(Session)
    yield sess
    sess.close()
    engine.dispose()


@pytest.fixture
def async_session():
    raise NotImplementedError('Async support in testing is pending')
    session = None
    yield session
    session.close()
