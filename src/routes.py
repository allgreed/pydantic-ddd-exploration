"""
Goal: this should be the most boring file in the entire project
"""
import datetime
from uuid import UUID, uuid4

from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db
from src.core import Event, Location, Weather, EventKind


the_router = APIRouter()


# TODO: get rid of the dupplication
from pydantic import BaseModel, PositiveInt, confloat, validator
class LocationViewModel(BaseModel):
    latitude: confloat(ge=-90,le=90)
    longitude: confloat(ge=-180,le=180)

    class Config:
        orm_mode = True
ABSOLUTE_ZERO_CELCIUS = -273.15
class WeatherViewModel(BaseModel):
    temperature_celcius: confloat(ge=ABSOLUTE_ZERO_CELCIUS)

    class Config:
        orm_mode = True
class EventViewModel(BaseModel):
    uuid: UUID
    date: datetime.date
    location: LocationViewModel
    weather: WeatherViewModel
    kind: EventKind
    people_count: PositiveInt
    secret_digest: str
    @validator("date")
    def date_cannot_be_in_the_future(cls, v):
        date_now = datetime.datetime.now().date()

        if v > date_now:
            raise ValueError("ensure this value is not in the future")

        return v

    class Config:
        orm_mode = True
class EventCreateViewModel(BaseModel):
    uuid: UUID
    date: datetime.date
    location: LocationViewModel
    weather: WeatherViewModel
    kind: EventKind
    people_count: PositiveInt
    secret_digest: str
    @validator("date")
    def date_cannot_be_in_the_future(cls, v):
        date_now = datetime.datetime.now().date()

        if v > date_now:
            raise ValueError("ensure this value is not in the future")

        return v

    class Config:
        orm_mode = True


# TODO: add proper, efficient, modular pagination
class EventManyViewModel(BaseModel):
    events: Sequence[EventViewModel]


events = [
    Event(uuid=uuid4(), date=datetime.datetime.now().date(), people_count=555, secret_digest="aaa",
        location=Location(latitude=5, longitude=-8), weather=Weather(temperature_celcius=15), kind=EventKind.PARTY),
]


# TODO: pack get_db into a dependency at a higher level? o.0
@the_router.get("/", response_model=EventManyViewModel)
def read_many(db: Session = Depends(get_db)):
    # TODO: make sure __initialised__ is not in response
    # TODO: maybe middleware

    return EventManyViewModel(events=events)


# TODO: use actual DB

@the_router.post("/", response_model=EventViewModel, status_code=201)
def create(data: EventCreateViewModel, db: Session = Depends(get_db)):
    # TODO: move this to factory
    new_event = Event(**data, uuid=uuid4())

    # TODO: move this to repository
    events.append(event)

    return new_event
