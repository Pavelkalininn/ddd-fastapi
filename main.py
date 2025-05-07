from fastapi import FastAPI, Request
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()



@app.get("/")
async def main(request: Request):
    return {"request": "request"}
