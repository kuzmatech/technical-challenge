import sys
from peewee import SqliteDatabase, Model, CharField, IntegerField, DecimalField, AutoField
from numbers import Real
from decimal import Decimal

if "pytest" in sys.modules:
  db = SqliteDatabase(":memory:")
else:
  db = SqliteDatabase("test.db")

class Product(Model):
  id = AutoField(primary_key=True)
  name = CharField()
  brand = CharField()
  price = DecimalField()
  currency = CharField(max_length=3)
  in_stock_quantity = IntegerField()

  class Meta:
    database = db

class StorageInstance:
  def __init__(self):
    self.db = db
    self.db.connect()
    self.db.create_tables([Product])

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
