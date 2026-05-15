import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from agones_python_sdk import ApiClient, Configuration
from agones_python_sdk.api.sdk_api import SDKApi

AGONES_SDK_HTTP_PORT = int(os.environ.get("AGONES_SDK_HTTP_PORT", "9358"))

config = Configuration(host=f"http://localhost:{AGONES_SDK_HTTP_PORT}")
client = ApiClient(config)
sdk = SDKApi(client)


async def _health_loop():
    while True:
        await asyncio.to_thread(sdk.health, {})
        await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(sdk.ready, {})
    health_task = asyncio.create_task(_health_loop())
    yield
    health_task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    print("Received request")
    await asyncio.sleep(15)
    print("Shutting down")
    await asyncio.to_thread(sdk.shutdown, {})
    
    return {"message": "done"}
