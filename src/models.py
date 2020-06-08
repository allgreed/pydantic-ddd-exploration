"""
Goal: a bridge between SQLAlchemy and Core
"""
from src.db import Base, UUID
from src.core import Event, EventKind, Location, Weather

    # TODO: add unique title on DB level
    # TODO: how to handle that

    # TODO: is "models" the best name? - how about repository?

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

    # TODO: actually write this up
    @classmethod
    def from_core(cls, e: Event) -> "User":
        return cls(uuid=u.uuid.bytes,
              )

    def to_core(self) -> Event:
        return CoreUser(
               id=uuid.UUID(bytes=self.uuid),
            )
