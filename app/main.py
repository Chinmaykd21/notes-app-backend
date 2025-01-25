from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "message": "Welcome to Real-Time Notes App!" }

@app.get("/health")
def health_check():
    return { "status": "ok" }
