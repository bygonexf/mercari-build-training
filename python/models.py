from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer)
    image_name = Column(String)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)