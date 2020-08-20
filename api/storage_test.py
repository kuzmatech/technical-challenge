from storage import StorageInstance, Product, User, GiftList
from decimal import Decimal

db = StorageInstance()
test_product = {
  "name": "Kettle",
  "brand": "George Foreman",
  "price": Decimal("50.00"),
  "currency": "GBP",
  "in_stock_quantity": 12
}
test_user = {
  "password": "T34andCrumpets"
}
class TestProducts:

  @staticmethod
  def example_product_save() -> Product:
    new_product = db.save_product(test_product["name"], test_product["brand"], test_product["price"], test_product["currency"], test_product["in_stock_quantity"])
    return new_product

  def test_save_product(self):
    new_product = TestProducts.example_product_save()
    assert isinstance(new_product, Product)

  def test_load(self):
    new_product = TestProducts.example_product_save()
    p_id = new_product.id
    loaded_product = db.load_product_by_id(p_id)
    assert p_id == loaded_product["id"]

  def test_update(self):
    prod = TestProducts.example_product_save()
    updated_values = {
      "id": prod.id,
      "in_stock_quantity": 24
    }
    success = db.update_product_from_dict(updated_values)
    assert success == True
    updated_product = Product.get(Product.id == prod.id)
    assert updated_product.in_stock_quantity == 24

class TestUser:

  @staticmethod
  def example_user_save() -> User:
    from random import random
    random_number = random()
    username = f"bigjoe{random_number}"
    password = test_user["password"]
    new_user = User.add_user(username=username, password=password)
    return new_user
  def test_create_user(self):
    new_user = TestUser.example_user_save()
    assert isinstance(new_user, User)
  def test_check_password(self):
    new_user = TestUser.example_user_save()
    password = test_user["password"]
    matched = db.check_password(new_user, password)
    assert matched == True

class TestGiftList:
  def test_create_gift_list(self):
    from datetime import datetime
    user = TestUser().example_user_save()
    due_date = datetime(2020, 12, 15)
    new_gift_list = db.create_new_gift_list(user, due_date)
    assert isinstance(new_gift_list, GiftList)
  def test_add_to_gift_list_by_id(self):
    from datetime import datetime
    user = TestUser().example_user_save()
    due_date = datetime(2020, 12, 15)
    example_gift_list = db.create_new_gift_list(user, due_date)
    glist_id = example_gift_list.id
    product = TestProducts().example_product_save()
    example_gift = {
      "product_id": product.id,
      "quantity": 5,
      "purchased": 0
    }
    success = db.add_gift_to_list_by_id(glist_id, example_gift)
    assert success == True
    product2 = TestProducts().example_product_save()
    example_gift2 = {
      "product_id": product2.id,
      "quantity": 7,
      "purchased": 0
    }
    success_two = db.add_gift_to_list_by_id(glist_id, example_gift2)
    assert success_two == True

  def test_gift_list_update(self):
    from datetime import datetime
    user = TestUser().example_user_save()
    due_date = datetime(2020, 12, 15)
    example_gift_list = db.create_new_gift_list(user, due_date)
    glist_id = example_gift_list.id
    product = TestProducts().example_product_save()
    example_gift = {
      "product_id": product.id,
      "quantity": 5,
      "purchased": 0
    }
    success = db.add_gift_to_list_by_id(glist_id, example_gift)
    assert success == True
    updated_gift = example_gift.copy()
    updated_gift["purchased"] = 2
    success = db.update_gift_in_list_by_id(glist_id, updated_gift)
    assert success == True
    updated_gift_list = GiftList.get(GiftList.id == glist_id)
    p_id = example_gift["product_id"]
    gift_from_list = updated_gift_list.gifts[f"{p_id}"]
    assert gift_from_list["purchased"] == 2
