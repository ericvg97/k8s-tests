import asyncio
import random   


from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

number = random.randint(1, 100)

requests_being_processed: int = 0

@app.get("/")
async def root():
    global requests_being_processed
    if requests_being_processed >= 1:
        return JSONResponse(status_code=503, content={"status": "busy"})
    requests_being_processed += 1
    await asyncio.sleep(15)

    requests_being_processed -= 1

    return {"message": f"Hello World 2 {number}"}

@app.get("/metrics")
async def metrics():
    return {"requests_being_processed": requests_being_processed}

@app.get("/ready")
async def ready():
    global requests_being_processed
    if requests_being_processed >= 1:
        return JSONResponse(status_code=503, content={"status": "busy"})
    return {"status": "ok"}