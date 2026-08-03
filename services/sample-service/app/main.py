from fastapi import FastAPI

app = FastAPI(title="Sample Service")

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello from AKS"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
