"""
Goal: assess if Pydantic can be used as a native concept to build domain models on
"""
import datetime
from uuid import UUID, uuid4
from enum import Enum

from pydantic.dataclasses import dataclass
from pydantic import confloat, PositiveInt, validator, constr


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
    # TODO: the constraints actually come from technical requirements (hash length) and should be enforced somewhere else, but how? 
    secret_digest: constr(min_length=64, max_length=64)

    @validator("date")
    def date_cannot_be_in_the_future(cls, v):
        date_now = datetime.datetime.now().date()

        if v > date_now:
            raise ValueError("ensure this value is not in the future")

        return v


def make_event(data: dict):
    _data = data.copy()

    uuid = uuid4()

    # TODO: actually use a "hashing" function
    secret_digest = "x" * 64

    del _data["secret"]

    return Event(**_data, uuid=uuid, secret_digest=secret_digest)
