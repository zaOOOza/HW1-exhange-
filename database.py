import os


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.environ.get('DB_CONNECTION_STR', 'postgresql://postgres:postgres@pg:5432/postgres'))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import model
    Base.metadata.create_all(bind=engine)
