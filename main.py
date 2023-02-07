from fastapi import FastAPI
from  router import locker

app = FastAPI()
app.include_router(locker.router)

@app.get("/")
def read_root():
    return {"msg": "Hello World"}
