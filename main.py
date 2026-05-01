import random

from fastapi import FastAPI

app = FastAPI()

number = random.randint(1, 100)

@app.get("/")
async def root():

    return {"message": f"Hello World 2 {number}"}