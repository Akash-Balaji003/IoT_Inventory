from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from DB_Interface import InventoryDB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

demoObj = InventoryDB("localhost", 3306, "root", "Akash003!", "IOT_Inventory")

@app.get("/test")
async def Test():
    return {"message": "Hello World!"}

@app.post("/borrow-device")
async def borrow_device_handler(request: Request):
    data = await request.json()
    return demoObj.borrow_device(data)
