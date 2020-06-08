"""
Goal: assess if Pydantic can be used as a native concept to build domain models on
"""
import datetime
from uuid import UUID
from enum import Enum

from pydantic.dataclasses import dataclass
from pydantic import confloat, PositiveInt, validator


from src.utils import hash_password



@dataclass
class Location:
    # domain constraints - earth is modeled as a sphere, etc etc
    # TODO: integrate this into a propper error message
    latitude: confloat(ge=-90,le=90)
    longitude: confloat(ge=-180,le=180)


ABSOLUTE_ZERO_CELCIUS = -273.15

@dataclass
class Weather:
    # cannot be less than absolute 0K
    # TODO: integrate this into a propper error message
    temperature_celcius: confloat(ge=ABSOLUTE_ZERO_CELCIUS)

class EventKind(str, Enum):
    PARTY = "party"
    GATHERING = "gathering"
    # TODO: I'd like this to be represent by int in DB and str in API


@dataclass
class Event:
    uuid: UUID

    date: datetime.date
    location: Location
    weather: Weather

    kind: EventKind
    people_count: PositiveInt
    secret_digest: str
    # TODO: add type safety to digest
    # TODO: add mypy
    # TODO: digest can be set via hashing

    @validator("date")
    def date_cannot_be_in_the_future(cls, v):
        date_now = datetime.datetime.now().date()

        if v > date_now:
            raise ValueError("ensure this value is not in the future")

        return v
