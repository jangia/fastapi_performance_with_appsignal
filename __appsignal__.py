import os

from appsignal import Appsignal

appsignal = Appsignal(
    active=True,
    name="fastapi_performance_with_appsignal",
    push_api_key=os.getenv("APPSIGNAL_PUSH_API_KEY"),
    revision="main",
    enable_host_metrics=True,
)
