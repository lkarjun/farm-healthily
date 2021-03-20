from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "Lalkrishan"}



if __name__ == "__main__":
    uvicorn.run(app)