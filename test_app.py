from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI works"}

@app.get("/hello")
def hello():
    return {"hello": "world"}