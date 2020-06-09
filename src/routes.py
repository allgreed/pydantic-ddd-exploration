"""
Goal: this should be the most boring file in the entire project
"""
import datetime
from uuid import UUID, uuid4
from typing import Sequence, Optional, Any

from fastapi import APIRouter, Depends
from pydantic import constr
from sqlalchemy.orm import Session

from src.db import get_db
from src.core import Event, Location, Weather, EventKind, make_event
from src.repositories import EventRepository


the_router = APIRouter()

def get_event_repository(db: Session = Depends(get_db)) -> EventRepository:
    return EventRepository(db)


# TODO: extract this to another file
import pydantic
import typing
# TODO: type domain model as Pydantic dataclass / Pydantic model
def viewmodel(domain_model: "any", omit_fields: Sequence[str] = ()):
    def class_decorator(cls):
        class MetaMeta(type(pydantic.BaseModel)):
            def __new__(_, __, ___, ____):
                    base = domain_model.__pydantic_model__
                    # TODO: implement better field omission - maybe create another base and copy everything but the omitted fields
                    # https://github.com/samuelcolvin/pydantic/blob/master/pydantic/main.py

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

                    for x in omit_fields:
                        _initial_annotations[x] = typing.Union[typing.Any, type(None)]

                    base_annotations = base.__annotations__
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

                    bases = (base, cls)
                    # avoid unnecessary calls to self
                    _meta = type(pydantic.BaseModel)

                    return super().__new__(_meta, cls.__qualname__, bases, dct)

        class ResultCls(metaclass=MetaMeta):
            # TODO: only overwrite this method if there are fields to be omitted
            def dict(*args, **kwargs):
                raise ValueError("BBBB")
            pass

        # break recursison
        f = ResultCls.dict
        def _dict(*args, **kwargs):
            kwargs["exclude"] = set(omit_fields)
            return f(*args, **kwargs)

        ResultCls.dict = _dict


        return ResultCls
    return class_decorator


@viewmodel(Location)
class LocationViewModel:
    pass


@viewmodel(Weather)
class WeatherViewModel:
    pass


@viewmodel(Event, omit_fields={"secret_digest"})
class EventViewModel:
    pass


@viewmodel(Event, omit_fields={"uuid", "secret_digest"})
class EventCreateViewModel:
    secret: constr(min_length=1, max_length=255)


@the_router.get("/", response_model=Sequence[EventViewModel])
def read_many(r: EventRepository = Depends(get_event_repository)):
    # TODO: make sure __initialised__ is not in response
    # TODO: maybe middleware

    with r.read() as r:
        return r.get_all()


@the_router.post("/", response_model=EventViewModel, status_code=201)
def create(data: EventCreateViewModel, r: EventRepository = Depends(get_event_repository)):
    new_event = make_event(data.dict())

    # this is just for demo purposes
    # TODO: remove this
    print(new_event.secret_digest)

    with r.write() as r:
        r.add(new_event)

    return new_event


# TODO: add put
# TODO: add patch
# TODO: add delete
