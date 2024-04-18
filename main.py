import uvicorn
from fastapi import FastAPI

test_app = FastAPI()

@test_app.get("/")
def central():
    return {"Jon" : "Slotved2"}

if __name__ == "__main__":
    uvicorn.run(test_app, port=8888, host="0.0.0.0")

