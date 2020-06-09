"""
Goal: a bridge between SQLAlchemy and Core
"""
import uuid
from typing import Sequence
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Float, String, Date, Enum

from src.db import Base, UUID
from src.core import Event, EventKind, Location, Weather

# TODO: add unique title on DB level
# TODO: how to handle that

class SqlEvent(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    uuid = Column(UUID(), nullable=False, index=True, unique=True)

    date = Column(Date, nullable=False)
    # TODO: how to handle nested things sensibly?
    location_latitude = Column(Float, nullable=False)
    location_longitude = Column(Float, nullable=False)
    weather_temperature_celcius = Column(Float, nullable=False)

    kind = Column(Enum(EventKind, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    people_count = Column(Integer, nullable=False)
    secret_digest = Column(String(length=60), nullable=False)

    # TODO: is there a point in automating this?
    @classmethod
    def from_core(cls, e: Event) -> "SqlEvent":
        return cls(uuid=e.uuid.bytes,
            date=e.date,
            location_latitude = e.location.latitude,
            location_longitude = e.location.longitude,
            weather_temperature_celcius = e.weather.temperature_celcius,
            kind = e.kind,
            people_count = e.people_count,
            secret_digest = e.secret_digest,
            )

    def to_core(self) -> Event:
        return Event(
               uuid=uuid.UUID(bytes=self.uuid),
               date=self.date,
               location=Location(latitude=self.location_latitude, longitude=self.location_longitude),
               weather=Weather(temperature_celcius=self.weather_temperature_celcius),
               people_count=self.people_count,
               secret_digest=self.secret_digest,
               kind=self.kind,
            )


class QueryEventRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self) -> Sequence[Event]:
        _events = self.db.query(SqlEvent).all()

        return list(map(lambda e: e.to_core(), _events))


class CommandEventRepository(QueryEventRepository):
    def __init__(self, db):
        self.db = db

    def add(self, e: Event):
        self.db.add(SqlEvent.from_core(e))


class EventRepository:
    def __init__(self, db):
        self.db = db

    @contextmanager
    def read(self):
        yield QueryEventRepository(self.db)

    @contextmanager
    def write(self):
        try:
            yield CommandEventRepository(self.db)
        finally:
            self.db.commit()
