#implement logging into crtical transaction features.
import logging as logger

#import the rest_framework library
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#import the models
from trxs.models import Trxs, TrxsReceipt
from inventories.models import Inventories
from stores.models import Stores

#import the serializers
from inventories.serializers import InventoriesSerializer
from trxs.serializers import TrxsSerializer, TrxsReceiptReadSerializer, TrxsReceiptPostSerializer

class TransactionEngine(APIView):
    #initiate a transaction_cache to store all the metadata needed for this transaction.
    def __init__(self):
        self.request_cache = {}

    # listen for the incoming post request
    def post(self,request,format=None):
        #create a hashmap of the incoming request post payload
        shopping_cart_hash = request.data
        #make a copy of the incoming_request and log it.
        self.request_cache["incoming_request"] = request.data
        #call the master handler
        return TransactionServiceHandler().master_engine_handler(shopping_cart_hash)

class TransactionMessages:
    #create a message of this transaction that needs to happen.
    def __init__(self):
        self.transaction_cache = {}
        self.final_response = {}

    # call this method to initially create a blank message.
    def initiate_message(self):
        #describing message structure type
        self.transaction_cache["incoming_request"] = None
        self.transaction_cache["store_id"] = None
        self.transaction_cache["master_trx_id"] = None
        self.transaction_cache["item_dollar_total"] = None
        self.transaction_cache["sales_tax_dollar"] = None
        self.transaction_cache["total_cost"] = None
        self.transaction_cache["cart_items"] = None
        self.transaction_cache["checked_out_item"] = []
        self.transaction_cache["bad_line_item"] = None

class FinalResponse:
    def __init__(self):
        self.final_response = {}
    # call this method to initially create a blank response.
    def initiate_response(self):
        self.final_response["message"] = "Success_or_Error"
        self.final_response["transaction"] = {
            "transaction_id": None,
            "missing_items": None,
                "total_cost": {
                    "tax_dollars" : None,
                    "item_dollars" : None,
                    "total_dollars" : None
                }
            }

class TransactionServiceHandler:
    def master_engine_handler(self,shopping_cart_hash):
        #this method can be refactored to make more DRY the get and set methods of the transaction message

        #create the transaction message object
        transaction_message = TransactionMessages()
        transaction_message.initiate_message()

        #populate the transaction_message
        transaction_message.transaction_cache["incoming_request"] = shopping_cart_hash
        transaction_message.transaction_cache["store_id"] = shopping_cart_hash["store"]
        transaction_message.transaction_cache["cart_items"] = shopping_cart_hash["cart_items"]

        #create the master transaction needed first.
        master_trx_id = self.retrieve_master_transaction(transaction_message)
        transaction_message.transaction_cache["master_trx_id"] = master_trx_id

        #initiate the subtransaction process
        sub_transaction_success = self.inventory_transaction_wrapper(transaction_message)

        if sub_transaction_success == "Master_Transaction_Success":
            final_transaction_cost = self.costing_handler(transaction_message)
        elif sub_transaction_success == "Master_Transaction_Error":
            final_transaction_cost = "Failure"

        # generate the expected return response
        return_response = self.final_payload_generator(transaction_message,final_transaction_cost)
        # return the response
        return return_response

    def retrieve_master_transaction(self,transaction_message):
        transaction_payload_store_id = transaction_message.transaction_cache["store_id"]
        transaction_payload = {
            "store":transaction_payload_store_id
            }
        trx_serializer = TrxsSerializer(data=transaction_payload)
        if trx_serializer.is_valid():
            trx_serializer.save()
        return trx_serializer.data['id']

    def inventory_transaction_wrapper(self,transaction_message):
        def inventory_check_looper(transaction_message,item_id,cart_quantity,reverse = False):
            try:
                inventory_line = Inventories.objects.get(store=transaction_message.transaction_cache["store_id"],item=item_id)
                current_quantity = inventory_line.quantity
                cart_quantity = int(cart_quantity)
                current_quantity -= cart_quantity
                inventory_payload = {
                    "store" : transaction_message.transaction_cache["store_id"],
                    "item" : item_id,
                    "quantity" : current_quantity
                }
                inventory_serializer_line = InventoriesSerializer(inventory_line,data=inventory_payload)
                if inventory_serializer_line.is_valid():
                    inventory_serializer_line.save()
                elif not inventory_serializer_line.is_valid():
                    #exception thrown here that quantity does not exist
                    inventory_serializer_line.save()
                # check if in commit mode or reverse mode
                if reverse == False:
                    # these items that have actually been checked_out and keep a record
                    inventory_payload["quantity"] = cart_quantity
                    transaction_message.transaction_cache["checked_out_item"].append(inventory_payload)
                return "Success"
            except:
                #reverse the inventory!
                bad_inventory_payload = {"store":transaction_message.transaction_cache["store_id"], "item":item_id, "quantity":cart_quantity}
                transaction_message.transaction_cache["bad_line_item"] = bad_inventory_payload
                inventory_reverser(transaction_message)
                #delete the master transaction!
                master_transaction_id_remove(transaction_message)
                return "Error"

        def inventory_reverser(transaction_message):
            checked_out_items = transaction_message.transaction_cache["checked_out_item"]
            for item_to_be_reversed in checked_out_items:
                store_id = item_to_be_reversed["store"]
                cart_item = item_to_be_reversed["item"]
                # make sure this is an int or can be integerized"
                # In order to reverse a transaction make it a negative number so -(-x) is +
                cart_quantity = -1 * int(item_to_be_reversed["quantity"])
                # run the inventory check in reverse
                success_inventory_entry = inventory_check_looper(transaction_message,cart_item,cart_quantity,True)

        def master_transaction_id_remove(transaction_message):
            trx = Trxs.objects.get(pk=transaction_message.transaction_cache["master_trx_id"])
            trx.delete()
            transaction_message.transaction_cache["master_trx_id"] = None
            return "master_id removed successfully from database"

        def transactions_check_looper(transaction_message,checked_out_item,checked_out_quantity):
            try:
                transaction_receipt_payload = {
                    "items" : checked_out_item,
                    "quantity" : checked_out_quantity,
                    "trxs" : transaction_message.transaction_cache["master_trx_id"]
                }
                serializer = TrxsReceiptPostSerializer(data=transaction_receipt_payload)
                if serializer.is_valid():
                    serializer.save()
                return "Success"
            except:
                return "Error"

        transaction_payload_store_id = transaction_message.transaction_cache["store_id"]
        shopping_cart_items = transaction_message.transaction_cache["cart_items"]


        for checkout_item in shopping_cart_items:
            cart_item = checkout_item["items_id"]
            # make sure this is an int or can be integerized"
            cart_quantity = checkout_item["quantity"]
            success_inventory_entry = inventory_check_looper(transaction_message,cart_item,cart_quantity)
            if success_inventory_entry != "Success":
                return "Master_Transaction_Error"

        for checkout_item in shopping_cart_items:
            cart_item = checkout_item["items_id"]
            # make sure this is an int or can be integerized"
            cart_quantity = checkout_item["quantity"]
            success_transaction_entry = transactions_check_looper(transaction_message,cart_item,cart_quantity)
            if success_transaction_entry != "Success":
                return "Master_Transaction_Error"
        return "Master_Transaction_Success"

    def costing_handler(self,transaction_message):
        def item_coster(transaction_message):
            trxreceipt_lines = TrxsReceipt.objects.filter(trxs_id=transaction_message.transaction_cache["master_trx_id"])
            sale_total = 0
            for trx_line in trxreceipt_lines:
                quantity_bought = trx_line.quantity
                item_price = trx_line.items.price
                sale_total += quantity_bought * item_price
            return sale_total

        def sales_tax_coster(transaction_message):
            current_store = Stores.objects.filter(id=transaction_message.transaction_cache["store_id"])
            tax_rate = current_store[0].local_tax
            sales_tax_dollars = tax_rate/100 * transaction_message.transaction_cache["item_dollar_total"]
            sales_tax_dollars = round(sales_tax_dollars,2)
            return sales_tax_dollars

        def transaction_cost_write(transaction_message):
            master_trx = Trxs.objects.get(pk=transaction_message.transaction_cache["master_trx_id"])
            master_trx_payload = {
                "tax_dollars" : round(transaction_message.transaction_cache["sales_tax_dollar"],2),
                "sale_dollars" : round(transaction_message.transaction_cache["item_dollar_total"],2),
                "sale_total" : round(transaction_message.transaction_cache["total_cost"],2),
                "store" : transaction_message.transaction_cache["store_id"]
            }
            serializer = TrxsSerializer(master_trx,data=master_trx_payload)
            if serializer.is_valid():
                serializer.save()
                return "Success"

        item_dollar_total = item_coster(transaction_message)
        transaction_message.transaction_cache["item_dollar_total"] = item_dollar_total
        sales_tax_total = sales_tax_coster(transaction_message)
        transaction_message.transaction_cache["sales_tax_dollar"] = sales_tax_total
        total_cost = transaction_message.transaction_cache["item_dollar_total"] + transaction_message.transaction_cache["sales_tax_dollar"]
        transaction_message.transaction_cache["total_cost"] = round(total_cost,2)
        return transaction_cost_write(transaction_message)

    def final_payload_generator(self,transaction_message,transaction_flag):
        return_response = FinalResponse()
        return_response.initiate_response()

        if transaction_flag == "Success":
            return_response.final_response["message"] = "Success"
            
        elif transaction_flag == "Failure":
            return_response.final_response["message"] = "Error"

        return_response.final_response["transaction"]["transaction_id"] = transaction_message.transaction_cache["master_trx_id"]
        return_response.final_response["transaction"]["missing_items"] = transaction_message.transaction_cache["bad_line_item"]
        return_response.final_response["transaction"]["total_cost"] = {
            "tax_dollars" : transaction_message.transaction_cache["sales_tax_dollar"],
            "item_dollars" : transaction_message.transaction_cache["item_dollar_total"],
            "total_dollars" : transaction_message.transaction_cache["total_cost"]
        }
        return Response(return_response.final_response,status=status.HTTP_400_BAD_REQUEST)
