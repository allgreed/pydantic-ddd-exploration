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


import pydantic

# TODO: type domain model as Pydantic dataclass / Pydantic model
def viewmodel(domain_model: "any"):
    def class_decorator(cls):
        class MetaMeta(type(pydantic.BaseModel)):
            def __new__(meta, name, bases, _dct):
                    #print(bases)

                    dct = {
                        "__module__": cls.__module__,
                        "__qualname__": cls.__qualname__,
                    }
                    if hasattr(cls, "Config"):
                        ...
                        #dct["Config"] = cls.Config
                        #Config.orm_mode = True
                    else:
                        class Config:
                            orm_mode = True

                        dct["Config"] = Config

                    _initial_annotations = {}

                    base_annotations = bases[0].__annotations__
                    for annotation_name, annotation in base_annotations.items():
                        # TODO: check for pydantic model / being core, etc
                        if annotation_name == "location" or annotation_name == "weather":
                            # TODO: what if not globals? o.0
                            t = globals().get(f"{annotation.__qualname__}ViewModel")
                            if t:
                                _initial_annotations[annotation_name] = t

                    if hasattr(cls, "__annotations__"):
                        _initial_annotations.update(cls.__annotations__)

                    dct["__annotations__"] = _initial_annotations


                    # avoid unnecessary calls to self
                    _meta = type(pydantic.BaseModel)
                    return super().__new__(_meta, cls.__qualname__, bases, dct)

        class ResultCls(domain_model.__pydantic_model__, metaclass=MetaMeta):
            pass
        return ResultCls
    return class_decorator


@viewmodel(Location)
class LocationViewModel:
    pass


@viewmodel(Weather)
class WeatherViewModel:
    pass


@viewmodel(Event)
class EventViewModel:
    pass

# TODO: get rid of the dupplication
from pydantic import BaseModel, PositiveInt, confloat, validator
class EventCreateViewModel(BaseModel):
    # TODO: allow for field omission, maybe create another base and copy everything but the ommited fields
    # https://github.com/samuelcolvin/pydantic/blob/master/pydantic/main.py
    __omit__ = {"uuid"}
    pass

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
# TODO: -- end of duplication --


class EventManyViewModel(BaseModel):
    events: Sequence[EventViewModel]


events = [
    Event(uuid=uuid4(), date=datetime.datetime.now().date(), people_count=555, secret_digest="aaa",
        location=Location(latitude=5, longitude=-8), weather=Weather(temperature_celcius=5), kind=EventKind.PARTY),
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
    new_event = Event(**data.dict(), uuid=uuid4())

    # TODO: move this to repository
    events.append(new_event)

    return new_event
