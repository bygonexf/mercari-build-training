import os
import logging
import pathlib
import json
import hashlib
from fastapi import FastAPI, Form, HTTPException, UploadFile
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
def get_items():
    items = json.loads(itemFile.read_text(encoding="utf-8"))
    return items

@app.get("/items/{idFrom1}")
def get_item(idFrom1: int):
    items = json.loads(itemFile.read_text(encoding="utf-8"))
    return items["items"][idFrom1-1]


@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...), image: UploadFile = Form(...)):
    logger.info(f"Receive item: {name}")

    imageBytes = image.file.read()
    hashed = hashlib.sha256(imageBytes).hexdigest()
    hashedImgName = hashed + os.path.splitext(image.filename)[1]
    hashedImgPath = images / hashedImgName
    hashedImgPath.touch(exist_ok= True)
    hashedImgPath.write_bytes(imageBytes)

    items["items"].append({"name": name, "category": category, "image": hashedImgName})
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
