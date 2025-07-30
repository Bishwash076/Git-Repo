from fastapi import FastAPI

app = FastAPI()

@app.get("/ask")
def ask(question: str):
    return {"answer": "This is a placeholder response"}
