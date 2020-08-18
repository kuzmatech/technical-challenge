from storage import StorageInstance, Product
from decimal import Decimal

test_product = {
  "name": "Kettle",
  "brand": "George Foreman",
  "price": Decimal("50.00"),
  "currency": "GBP",
  "in_stock_quantity": 12
}
db = StorageInstance()
def example_product_save():
  new_product = db.save_product(test_product["name"], test_product["brand"], test_product["price"], test_product["currency"], test_product["in_stock_quantity"])
  return new_product

def test_save_product():
  new_product = example_product_save()
  assert isinstance(new_product, Product)

def test_load():
  new_product = example_product_save()
  p_id = new_product.id
  loaded_product = db.load_product_by_id(p_id)
  assert p_id == loaded_product["id"]

def test_update():
  prod = example_product_save()
  updated_values = {
    "id": prod.id,
    "in_stock_quantity": 24
  }
  success = db.update_product_from_dict(updated_values)
  assert success == True
  updated_product = Product.get(Product.id == prod.id)
  assert updated_product.in_stock_quantity == 24
