import os
import logging
import pathlib
import json
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
curDir = pathlib.Path(__file__).parent.resolve()
images = curDir / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

itemFile = curDir / "items.json"
if os.stat(itemFile).st_size != 0:
    items = json.loads(itemFile.read_text(encoding="utf-8"))
else:
    items = {"items": []}

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def root():
    items = json.loads(itemFile.read_text(encoding="utf-8"))
    return items


@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
    logger.info(f"Receive item: {name}")
    items["items"].append({"name": name, "category": category})
    itemFile.write_text(json.dumps(items), encoding='utf-8')
    return {"message": f"item received: {name}"}


@app.get("/image/{image_name}")
async def get_image(image_name):
    # Create image path
    image = images / image_name

    if not image_name.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
