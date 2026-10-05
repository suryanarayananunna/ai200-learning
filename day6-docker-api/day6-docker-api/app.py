from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello from my AI-200 Docker API!"}


@app.get("/health")
def health():
    return {"status": "healthy"}