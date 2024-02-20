from sqlalchemy.orm import Session

from models import Item, Category
import schemas

def getItems(db: Session):
    res = db.query(Item.id, Item.name, Category.name.label("category"), Item.image_name).join(Category, Item.category_id==Category.id).all()
    return res

def getItemsBySearch(db: Session, keyword: str):
    res = db.query(Item.id, Item.name, Category.name.label("category"), Item.image_name).filter(Item.name.contains(keyword)).join(Category, Item.category_id==Category.id).all()
    return res

def createItem(db: Session, item: schemas.ItemCreate):
    curItem = Item(name=item.name, category_id=item.category_id, image_name=item.image_name)
    db.add(curItem)
    db.commit()
    db.refresh(curItem)

    return curItem