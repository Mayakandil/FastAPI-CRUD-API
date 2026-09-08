from fastapi import FastAPI
app = FastAPI()
@app.get("/") # "@" decorator , takes the function below and does something with it , in this case --> path "/" operation "get" decorator "@"
async def root(): # async == in hury , momken nshelha 3ady 
    return {"message":"Hello World"}