# from main import app
from src.database.db import db
from sqlalchemy import Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY

class Menu(db.Model):
    __tablename__="menus"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=True)
    category = db.Column(String, nullable=True)
    calories = db.Column(Float, nullable=True)
    price = db.Column(Float, nullable=True)
    description = db.Column(String, nullable=True)
    ingredients = db.Column(ARRAY(String))

# if __name__=="__main__":
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
