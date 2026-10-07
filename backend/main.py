from fastapi import FastAPI

app = FastAPI(title="COVERTEX")

@app.get("/")
def home():
    return {
        "project": "COVERTEX",
        "status": "running"
    }