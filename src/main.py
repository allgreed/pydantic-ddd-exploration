# TODO: use a __main__ file? See Upgrade's toy project

from fastapi import FastAPI


app = FastAPI()

from src.routes import the_router
app.include_router(the_router)
