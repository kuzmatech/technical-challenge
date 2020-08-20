from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser
from flask_jwt import jwt_required, current_identity
from storage import GiftList

#Gift List Post Argument Handler
giftlist_create_request_parser = RequestParser()
giftlist_create_request_parser.add_argument("due", type=str, required=True, help="Due date needs to be provided.")
giftlist_create_request_parser.add_argument("gifts", type=dict)
#Gift List Put Argument Handler
giftlist_update_request_parser = RequestParser()
giftlist_update_request_parser.add_argument("gifts", type=dict)
giftlist_update_request_parser.add_argument("due", type=str)

class GiftListView(Resource):
  def get(self, g_id: int):
    from storage import GiftList
    gift_dict = {}
    try:
      gift_list = GiftList.get(GiftList.id == g_id)
      gift_dict = gift_list.to_dict()
    except GiftList.DoesNotExist:
      abort(404, message="Gift list not found.")
    return gift_dict
  @jwt_required()
  def post(self):
    from main import db
    args = giftlist_create_request_parser.parse_args()
    due = args["due"]
    gifts = args["gifts"]
    from datetime import datetime
    user = current_identity.get()
    due_date = datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
    new_gift_list = db.create_new_gift_list(user, due_date, gifts)
    return_dict = new_gift_list.to_dict()
    return return_dict
  @jwt_required()
  def put(self, g_id: int):
    current_user = current_identity.get()
    args = giftlist_update_request_parser.parse_args()
    gift_list_id = g_id
    updated_gifts = args["gifts"]
    due = args["due"]
    try:
      g_list = GiftList.get(GiftList.id == gift_list_id)
    except GiftList.DoesNotExist:
      abort(404, message="Gift list not found.")
    if current_user != g_list.user:
      abort(401, message="Must be the owner of a gift list to modify.")
    if updated_gifts is not None or updated_gifts is not {}:
      g_list.gifts = updated_gifts
      g_list.save()
    if due is not None or "":
      from datetime import datetime
      due_date = datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
      g_list.due = due_date
      g_list.save()
    updated_g_list = g_list.get()
    return updated_g_list.to_dict()
