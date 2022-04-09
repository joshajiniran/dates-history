from fastapi import FastAPI

app = FastAPI()


# sanity check route
@app.get("/ping")
def pong():
    return {"ping": "pong!"}
