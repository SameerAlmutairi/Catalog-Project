from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Create USER table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    photo = Column(String(250), nullable=False)


class Catalog(Base):
    __tablename__ = 'catalog'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    photo = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'photo': self.photo,
        }

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    # photo = Column(String(250), nullable=False)
    price = Column(Float, nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog, backref='items')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
        }


class ItemPhotos(Base):
    __tablename__ = 'item_photos'
    id = Column(Integer, primary_key=True)
    photo_url = Column(String(250), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'))
    items = relationship(Items, backref='item_photos')
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog, backref='item_photos')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'photo_url': self.photo_url,
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)

