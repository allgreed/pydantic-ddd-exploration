import os
import sys

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Binary, TypeDecorator
from sqlalchemy.orm import sessionmaker


try:
    DATABASE_CONNECTION_STRING = os.environ.get("DATABASE_CONNECTION_STRING", f"sqlite:///{os.getcwd()}/bd.db")
except KeyError as e:
    print(f"Missing required environment variable {e}", file=sys.stderr)
    exit(1)

engine = create_engine(DATABASE_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UUID(TypeDecorator):
    impl = Binary


def setup_db():
    # need to evaluate table definitions
    import src.main

    Base.metadata.create_all(engine)
