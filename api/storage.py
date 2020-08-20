import sys, bcrypt
from numbers import Real
from decimal import Decimal
from typing import Tuple
from peewee import SqliteDatabase, Model, CharField, IntegerField, DecimalField, AutoField, ForeignKeyField, DateTimeField
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField
from datetime import datetime

if "pytest" in sys.modules:
  db = SqliteExtDatabase(":memory:")
else:
  db = SqliteExtDatabase("test.db")

class Product(Model):
  id = AutoField(primary_key=True)
  name = CharField()
  brand = CharField()
  price = DecimalField()
  currency = CharField(max_length=3)
  in_stock_quantity = IntegerField()

  class Meta:
    database = db

class User(Model):
  id = AutoField(primary_key=True)
  username = CharField(unique=True)
  password = CharField()

  @staticmethod
  def add_user(username: str, password: str):
    salt = bcrypt.gensalt()
    pass_bytes = password.encode('utf-8')
    hashed_pass = bcrypt.hashpw(pass_bytes, salt)
    new_user = User.create(username=username, password=hashed_pass)
    return new_user

  class Meta:
    database = db

class GiftList(Model):
  id = AutoField(primary_key=True)
  user = ForeignKeyField(User, backref='giftlist', unique=True)
  created = DateTimeField()
  due = DateTimeField()
  gifts = JSONField(null = True)

  def to_dict(self) -> dict:
    return_dict = {}
    return_dict["id"] = self.id
    return_dict["created"] = f"{self.created}"
    return_dict["due"] = f"{self.due}"
    return_dict["gifts"] = self.gifts
    return return_dict

  class Meta:
    database = db

class StorageInstance:
  def __init__(self):
    self.db = db
    self.db.connect(reuse_if_open=True)
    self.db.create_tables([Product, User, GiftList])

  def save_product(self, product_name: str, product_brand: str, product_price: Real, product_currency: str , product_stock: int) -> Product:
    new_product = Product.create(name=product_name, brand=product_brand, price=product_price, currency=product_currency, in_stock_quantity=product_stock)
    return new_product

  def load_product_by_id(self, product_id: int) -> dict:
    product_model = Product.get(Product.id == product_id)
    product = {
      "id": product_model.id,
      "name": product_model.name,
      "brand": product_model.brand,
      "price": Decimal(product_model.price),
      "currency": product_model.currency,
      "in_stock_quantity": product_model.in_stock_quantity
    }
    return product
  
  def update_product_from_dict(self, p_dict: dict) -> Product:
    p_id = p_dict["id"]
    with db.atomic() as transaction:
      query = Product.update(p_dict).where(Product.id == p_id)
      if query.execute() != 1:
        # If anything other than one row is being updated, there's an issue in the data so we'll return false
        # Any other errors can be caught and handled elsewhere
        transaction.rollback()
        return False
    return True

  def check_password(self, user: User, password: str) -> bool:
    user_pass = user.password
    pass_bytes = password.encode('utf-8')
    return bcrypt.checkpw(pass_bytes, user_pass)

  def __add_gift_to_list(self, gift_list: GiftList, gift: dict) -> bool:
    gift_id = gift["product_id"]
    gift_list_id = gift_list.id
    if gift_list.gifts is not None:
      query = GiftList.update(gifts=GiftList.gifts.update({f"{gift_id}": gift})).where(GiftList.id == gift_list_id)
      query.execute()
    else:
      gift_list.gifts = {f"{gift_id}": gift}
      gift_list.save()
    return True
  
  def __update_gift_in_list_by_id(self, gift_list_id: int, gift: dict) -> bool:
    gift_id = gift["product_id"]
    query = GiftList.update(gifts=GiftList.gifts[f"{gift_id}"].set(gift)).where(GiftList.id == gift_list_id)
    query.execute()
    return True

  def create_new_gift_list(self, user: User, due_date: datetime, gifts: dict = {}) -> GiftList:
    current_datetime = datetime.now()
    new_gift_list = GiftList.create(user=user, created=current_datetime, due=due_date, gifts=gifts)
    return new_gift_list

  def add_gift_to_list_by_id(self, gift_list_id: int, gift_dict: dict) -> bool:
    gift_list = GiftList.get(GiftList.id == gift_list_id)
    success = self.__add_gift_to_list(gift_list, gift_dict)
    return success
  
  def update_gift_in_list_by_id(self, gift_list_id: int, gift_dict: dict) -> bool:
    success = self.__update_gift_in_list_by_id(gift_list_id, gift_dict)
    return success
