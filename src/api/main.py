from fastapi import FastAPI

app = FastAPI()


# sanity check route
@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
