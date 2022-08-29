import asyncio
from http import HTTPStatus

from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .routers import pieces, subpieces, schedules
from .database import SessionLocal, engine
from .internal.admin import PieceAdmin, SubPieceAdmin, ScheduleAdmin
from .core.helpers import (
    all_stop_playing,
    close_stream,
    set_playback_speed,
    get_current_state,
)
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Relay Performer")

app.include_router(pieces.router)
app.include_router(subpieces.router)
app.include_router(schedules.router)

# Admin
admin = Admin(app, engine, title="Relay Performer", debug=True)
admin.add_view(PieceAdmin)
admin.add_view(SubPieceAdmin)
admin.add_view(ScheduleAdmin)


@app.patch("/stop", tags=["Interactive API"])
def stop_all_tasks():
    all_stop_playing()
    close_stream()
    return {"response": "all stop playing & recording"}


@app.patch("/speed", status_code=HTTPStatus.ACCEPTED, tags=["Interactive API"])
def update_speed(speed: float):
    set_playback_speed(speed)
    return {"response": f"update playback speed to {speed}"}


@app.get("/current-state", tags=["Basic API"])
def current_state():
    return get_current_state()


@app.get("/", tags=["Basic API"])
def root():
    return RedirectResponse("/docs")


@app.get("/test", tags=["Test"])
def test():
    print("test API for synchronous request")
    return {"hello": "world"}


@app.get("/async-test", tags=["Test"])
async def async_test():
    print("test API for asynchronous request - sleep for 0.1 sec...")
    await asyncio.sleep(0.1)
    return {"async hello": "world"}
