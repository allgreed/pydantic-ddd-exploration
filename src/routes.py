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
from src.core import Event, Location, Weather, EventKind, make_new_event
from src.repositories import EventRepository
from src.secrets import TheSecret


the_router = APIRouter()

def get_event_repository(db: Session = Depends(get_db)) -> EventRepository:
    return EventRepository(db)


# TODO: extract this to DDD
import pydantic
import typing
# TODO: type domain model as Pydantic dataclass / Pydantic model
def viewmodel(domain_model: "any", omit_fields: Sequence[str] = ()):
    def class_decorator(cls):
        class MetaMeta(type(pydantic.BaseModel)):
            def __new__(_, __, ___, original_dict):
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

                    for annotation_name, annotation in base.__annotations__.items():
                        # TODO: how does this work with pydantic.BaseModel ?
                        if hasattr(annotation, "__pydantic_model__"): # is pydantic model
                            # TODO: what if not globals? o.0
                            t = globals().get(f"{annotation.__qualname__}ViewModel")

                            if t and annotation is t.__domain_model__:
                                _initial_annotations[annotation_name] = t

                    if hasattr(cls, "__annotations__"):
                        _initial_annotations.update(cls.__annotations__)

                    dct["__annotations__"] = _initial_annotations

                    original_dict.pop("__module__")
                    original_dict.pop("__qualname__")

                    # avoid unnecessary calls to self
                    _meta = type(pydantic.BaseModel)
                    bases = (base, cls)

                    original_dict.update(dct)
                    _dict = original_dict

                    return super().__new__(_meta, cls.__qualname__, bases, _dict)

        # TODO: do I try to put stuff here or just handle this at the MetaMeta level?
        class ResultCls(metaclass=MetaMeta):
            __domain_model__ = domain_model

            # TODO: only overwrite this method if there are fields to be omitted
            def dict(self, *args, **kwargs):
                kwargs["exclude"] = set(omit_fields)
                return super().dict(*args, **kwargs)

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
    secret: TheSecret.RawType


@the_router.get("/", response_model=Sequence[EventViewModel])
def read_many(r: EventRepository = Depends(get_event_repository)):
    with r.read() as r:
        return r.get_all()


@the_router.post("/", response_model=EventViewModel, status_code=201)
def create(data: EventCreateViewModel, r: EventRepository = Depends(get_event_repository)):
    new_event = make_new_event(data.dict())

    with r.write() as r:
        r.add(new_event)

    return new_event


# TODO: add put
# TODO: add patch
# TODO: add delete
