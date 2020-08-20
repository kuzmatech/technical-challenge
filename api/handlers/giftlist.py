from typing import Union
from storage import GiftList, StorageInstance, Product

def purchase_gift(gift_list: GiftList, gift_id: int, quantity: int = 1) -> Union[bool, int]:
  from main import db
  if f"{gift_id}" not in gift_list.gifts:
    raise ValueError
  gift_list_entry = (gift_list.gifts[f"{gift_id}"]).copy()
  product = Product.get(Product.id == gift_id)
  try:
    product.purchase(quantity)
  except Product.OutOfStockError as err:
    return err.available
  gift_list_entry["purchased"] += quantity
  db.update_gift_in_list_by_id(gift_list.id, gift_list_entry)
  # {TODO}:
  # Log purchase history
  return True
