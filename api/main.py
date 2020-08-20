from os import environ
from flask import Flask, Response, make_response, jsonify, request
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from storage import StorageInstance
from handlers import authenticator
from views.giftlist import GiftListView

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = environ.get('TC_SECRET_KEY') or ''
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
api = Api(app, prefix="/api")
authenticate = authenticator.check_login_details
identity = authenticator.identity
db = StorageInstance()
jwt = JWT(app, authenticate, identity)
@app.errorhandler(403)
def forbidden(msg):
    return make_response(jsonify({"message": msg}), 403)

api.add_resource(GiftListView, '/gift_list', '/gift_list/<int:g_id>')

if __name__ == '__main__':
  from storage import User, Product
  try:
    User.get(User.username == "test_user")
  except User.DoesNotExist:
    User.add_user("test_user", "example_pass_5")
  example_products = [
    {
      "id": 1,
      "name": "Tea pot",
      "brand": "Le Creuset",
      "price": "47.00GBP",
      "in_stock_quantity": 50
    },
    {
      "id": 2,
      "name": "Cast Iron Oval Casserole - 25cm; Volcanic",
      "brand": "Le Creuset",
      "price": "210.00GBP",
      "in_stock_quantity": 27
    },
    {
      "id": 4,
      "name": "Gordon Ramsay Maze 12 Piece Set, White",
      "brand": "ROYAL DOULTON",
      "price": "85.00GBP",
      "in_stock_quantity": 2
    },
    {
      "id": 5,
      "name": "9-speed Hand Mixer; Almond Cream",
      "brand": "KITCHENAID",
      "price": "99.99GBP",
      "in_stock_quantity": 9
    },
    {
      "id": 6,
      "name": "Mini Stand Mixer; Empire Red",
      "brand": "KITCHENAID",
      "price": "399.00GBP",
      "in_stock_quantity": 2
    },
    {
      "id": 7,
      "name": "50's Style Stand Mixer, Full-Colour White",
      "brand": "SMEG SMALL APPLIANCES",
      "price": "449.00GBP",
      "in_stock_quantity": 0
    },
    {
      "id": 8,
      "name": "50's Style Stand Mixer, Black",
      "brand": "SMEG SMALL APPLIANCES",
      "price": "449.99GBP",
      "in_stock_quantity": 1
    },
    {
      "id": 9,
      "name": "Polka Bedding Set, King, Silver",
      "brand": "BEAU LIVING",
      "price": "105.00GBP",
      "in_stock_quantity": 5
    },
    {
      "id": 10,
      "name": "Paignton Bedding Set, King, White",
      "brand": "BEAU LIVING",
      "price": "105.00GBP",
      "in_stock_quantity": 0
    },
    {
      "id": 11,
      "name": "Original Kettle E-5710 Charcoal Barbecue - 57cm; Black",
      "brand": "WEBER GRILLS",
      "price": "199.99GBP",
      "in_stock_quantity": 1
    },
    {
      "id": 12,
      "name": "Compact Charcoal Grill, 57 cm",
      "brand": "WEBER GRILLS",
      "price": "139.99GBP",
      "in_stock_quantity": 29
    },
    {
      "id": 13,
      "name": "Falcon T2 Square Parasol, 2.7m, Taupe",
      "brand": "GARDENSTORE",
      "price": "344.99GBP",
      "in_stock_quantity": 5
    },
    {
      "id": 14,
      "name": "Riva Round Parasol - 3m; Anthracite",
      "brand": "GARDENSTORE",
      "price": "79.99GBP",
      "in_stock_quantity": 8
    },
    {
      "id": 15,
      "name": "Glow Challenger T2 Square Parasol - 3m, Taupe",
      "brand": "GARDENSTORE",
      "price": "619.99GBP",
      "in_stock_quantity": 30
    },
    {
      "id": 16,
      "name": "Ceramic Bottle Lamp, Small",
      "brand": "THE WHITE COMPANY",
      "price": "95.00GBP",
      "in_stock_quantity": 0
    },
    {
      "id": 17,
      "name": "Gold Sitting Mouse Lamp",
      "brand": "GRAHAM & GREEN",
      "price": "73.00GBP",
      "in_stock_quantity": 3
    },
    {
      "id": 18,
      "name": "Usha Mango Wood Lamp Base",
      "brand": "NKUKU",
      "price": "49.95GBP",
      "in_stock_quantity": 12
    },
    {
      "id": 19,
      "name": "Sea Green Honeycomb Glass Lamp",
      "brand": "GRAHAM & GREEN",
      "price": "95.00GBP",
      "in_stock_quantity": 4
    },
    {
      "id": 20,
      "name": "Faux Tortoiseshell Lamp",
      "brand": "OKA",
      "price": "175.00GBP",
      "in_stock_quantity": 0
    },
    {
      "id": 21,
      "name": "2 Person Blue Tweed Hamper",
      "brand": "WILLOW STORE",
      "price": "85.50GBP",
      "in_stock_quantity": 2
    }
  ]
  for e_product in example_products:
    p_id = e_product["id"]
    try:
      Product.get(Product.id == p_id)
    except Product.DoesNotExist:
      from decimal import Decimal
      product_name = e_product["name"]
      product_brand = e_product["brand"]
      product_price_string = f"{e_product['price']}"
      product_price = Decimal(product_price_string[:-3])
      product_currency = product_price_string[-3:]
      product_in_stock_quantity = e_product["in_stock_quantity"]
      db.save_product(product_name, product_brand, product_price, product_currency, product_in_stock_quantity)
  app.run(host='127.0.0.1', port=4924, debug=True)
