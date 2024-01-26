import json
import random
import time

import requests

from appsignal import set_category, set_sql_body, set_body
from fastapi import FastAPI, Depends
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sqlalchemy.orm import Session

from __appsignal__ import appsignal
from models import SessionLocal, Task

appsignal.start()

tracer = trace.get_tracer(__name__)

app = FastAPI(
    title="FastAPI with AppSignal",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello-world")
def hello_world():
    time.sleep(random.random())
    return {"message": "Hello World"}


@app.get("/error")
def error():
    raise Exception("Something went wrong. Oops!")


@app.get("/slow-external-api")
def slow_external_api():
    api_url = "http://docs.appsignal.com/"
    with tracer.start_as_current_span("Call External API"):
        set_category("external_api.http")
        set_body(json.dumps({"url": api_url}))
        requests.get(api_url)

    return {"message": "External API successfully called!"}


@app.get("/slow-query")
def slow_query(db: Session = Depends(get_db)):

    with tracer.start_as_current_span("List tasks"):
        query = db.query(Task)
        tasks = query.all()
        set_category("tasks.sql")
        set_sql_body(str(query))
    return {
        "tasks": [
            {"id": task.id, "title": task.title, "status": task.status}
            for task in tasks
        ],
    }


FastAPIInstrumentor().instrument_app(app)
