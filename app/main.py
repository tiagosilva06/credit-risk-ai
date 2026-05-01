from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def rota(): 
    return {"status": "Ok"}