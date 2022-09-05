import asyncio
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqladmin import Admin

from . import models
from .core.helpers import (all_stop_playing, close_stream, get_current_state,
                           set_playback_speed)
from .database import engine
from .redis import redis_client
from .internal.admin import PieceAdmin, ScheduleAdmin, SubPieceAdmin
from .routers import pieces, schedules, subpieces

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


# Test APIs
@app.get("/test", tags=["Test"])
def test():
    print("test API for synchronous request")
    return {"hello": "world"}


@app.get("/async-test", tags=["Test"])
async def async_test():
    print("test API for asynchronous request - sleep for 0.1 sec...")
    await asyncio.sleep(0.1)
    return {"async hello": "world"}


@app.get("/redis-test", tags=["Test"])
def redis_test(value: float = 1):
    redis_client.set("key", value)
    value = redis_client.get("key")
    return {"key": value}
