import os
import requests
import json
from prospereality_api.settings import PAYSTACK_SECRET_KEY

class PaystackRequestService:
    def __init__(self):
        self.URL = "https://api.paystack.co/"
        self.headers = {"Authorization": "Bearer {}".format(PAYSTACK_SECRET_KEY)}


    def post(self,endpoint: str, data: dict):
        return requests.post(self.URL + endpoint, json=data, headers=self.headers)


    def get(self,endpoint: str, params: dict = None):
        return requests.get(self.URL + endpoint, params=params, headers=self.headers)

class PaystackPaymentService:
    def __init__(self):
        self.requestService=PaystackRequestService()

    def initialize_transaction(self,**body):
        """
        Initialize a transaction to a customer;
        Important params -> amount, email, channels, metadata
        """
        try:
            endpoint = "transaction/initialize"
            body = {**body}
            resp = self.requestService.post(endpoint, body)
            if str(resp.status_code)[0] == "2":
                resp_data = resp.json()["data"]
                return resp_data
            raise RuntimeError(json.loads(resp.content)["message"])
        except Exception as e:
            raise RuntimeError("@initialize_transaction -> ", e)
        

    def verify_transaction(self,reference: str):
        """
        Verify the status of an initiated transaction;
        Important params -> reference
        """
        try:
            endpoint = "transaction/verify/{}".format(reference)
            resp = self.requestService.get(endpoint)
            if str(resp.status_code)[0] == "2":
                resp_data = resp.json()["data"]
                return resp_data
            return None

        except Exception as e:
            print(e)
            return None
        
