import os
import logging
import pathlib
import json
import hashlib
from typing import List
from fastapi import FastAPI, Form, HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import schemas
import dal
from database import SessionLocal

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = dal.getItems(db)

    return [r._asdict() for r in items]

@app.get("/items/search")
def get_items_by_search(keyword: str, db: Session = Depends(get_db)):
    items = dal.getItemsBySearch(db, keyword)

    return [r._asdict() for r in items]


@app.post("/items", response_model=schemas.Item)
def add_item(name: str = Form(...), category_id: int = Form(...), image: UploadFile = Form(...), db: Session = Depends(get_db)):
    logger.info(f"Receive item: {name}")

    imageBytes = image.file.read()
    hashed = hashlib.sha256(imageBytes).hexdigest()
    hashedImgName = hashed + os.path.splitext(image.filename)[1]
    hashedImgPath = images / hashedImgName
    hashedImgPath.touch(exist_ok= True)
    hashedImgPath.write_bytes(imageBytes)

    curItem = schemas.ItemCreate(name=name, category_id=category_id, image_name=hashedImgName)
    createdItem = dal.createItem(db, curItem)
    return createdItem


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
