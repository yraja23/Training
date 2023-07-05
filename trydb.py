# new branch 
import configparser
import os, getpass, argparse, sys
import time
from rasa_sdk import Tracker
# from configparser_crypt import ConfigParserCrypt
# from cryptography.fernet import Fernet
import requests,json,PyPDF2,yaml
from collections import Counter
from typing import Any, Text, Dict, List
from bardapi import Bard
class jsonConversion:
    def __init__(self, client_id, client_secret, access_token_url, scope):
            self.client_id = client_id
            self.client_secret = client_secret
            self.access_token_url = access_token_url
            self.scope = scope
    def generate_token(self):
        print("inside generate token")
        # Set the request parameters
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        # Send the request to obtain the access token
        response = requests.post(self.access_token_url, headers=headers, data=data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print('Error generating in access token:', response.text)
            return None
        
    def get_api_response_usecase3(self,access_token,item_loc):
        self.item_loc = item_loc
        # item1=tracker.get_slot('item_loc')
        # print()
        # loc = input("Enter location: ")
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item_loc}'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        
        if response.status_code == 200:
            api_response = response.json()
            items = api_response.get('items', [])
            output=""
            
            for item_data in items:
                if item_data.get('item') == item_loc:
                    item_no = item_data.get('item')
                    location = item_data.get('location')
                    location_type = item_data.get('loctype')
                    price = item_data.get('price')
                    
                    output += f"item_no: {item_no}\n"
                    output += f"location: {location}\n"
                    output += f"location_type: {location_type}\n"
                    output += f"price: {price}\n\n"
            
            if output:
                return output
            else:
                output_error = "No details exist for the given item. You can try searching for different items."
                return output_error
    
    def get_api_response(self,access_token,item,loc):
        self.item=item
        self.loc=loc
        # print(self.item)
        # print(self.loc)
        # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item}&location={self.loc}'
        # Make the API request with the access token
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()
            # print(api_response)
            items = api_response.get('items', [])
            output=""
            for item_data in items:
                # print("inside trydb function")
                if (item_data.get('item') == self.item and item_data.get('location')== int(self.loc)):
                    # print("Item and location match the response.")
                    item_no=item_data.get('item')
                    location=item_data.get('location')
                    location_type=item_data.get('loctype')
                    price=item_data.get('price')
                    output += f"item_no: {item_no}\nlocation: {location}\nlocation_type: {location_type}\nprice: {price}"
                    print(output)                   
            if output:
                return output
            else:         
                return None
    
            
    def get_api_response_usecase1(self, access_token):
        print("inside generate token")
        # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL
        API_ENDPOINT = 'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&limit=10'
        # Make the API request with the access token
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()
            items = api_response.get('items', [])
            output=""
            for item_data in items:
                # print("Item and location match the response.")
                item_no=item_data.get('item')
                location=item_data.get('location')
                location_type=item_data.get('loctype')
                price=item_data.get('price')
                output += f"\nitem_no: {item_no}\n"
                output += f"location: {location}\n"
                output += f"location_type: {location_type}\n"
                output += f"price: {price}\n\n"
                # print(output)
            if output:
                return output
            else:
                # Error occurred
                print('Error:', response.text)
                return None
class allFunc:
    def call_chatgpt_api(self, user_input: Text) -> Text:
        os.environ['_BARD_API_KEY']="XwiGpVdY-fzwrhRufLfzaJfmqh2dWi0Z47EeFwolwla9IJ9BBOK1q0HE0O7VpNTVoL1FCQ."
        answer = Bard().get_answer(user_input)['content']
        return answer
  #new - XwiGpVdY-fzwrhRufLfzaJfmqh2dWi0Z47EeFwolwla9IJ9BBOK1q0HE0O7VpNTVoL1FCQ.
  #old - XwiGpVdY-fzwrhRufLfzaJfmqh2dWi0Z47EeFwolwla9IJ9BBOK1q0HE0O7VpNTVoL1FCQ.
    
    
    
    # def resetSlotValues(self, user_input):
    #     self.user_input = user_input
    #     yes_answers = [
    #                 "Yes",
    #                 "Sure",
    #                 "Absolutely",
    #                 "Yeah",
    #                 "Of course",
    #                 "Definitely",
    #                 "OK"
    #             ]
    #     no_answers = [
    #             "No",
    #             "No, thanks",
    #             "Not now",
    #             "I don't want to",
    #             "No, I want something different",
    #             "No, change it up",
    #             "Skip",
    #             "Next",
    #             "Other steps, please"
    #         ]
        
    #     if self.user_input in yes_answers:
    #         print("yes returned")
    #         user_input = "yes"
    #         return user_input
    #     elif self.user_input in no_answers:
    #         user_input = "no"
    #         print("no returned")
    #         return user_input
        # else:
        #     else_val = input("Sorry, i could not understand. could you type yes or no?")
        #     return else_val
            
    # def get_api_response_usecase3(self,access_token,item_loc):
    #     self.item_loc = item_loc
    #     # item1=tracker.get_slot('item_loc')
    #     # print()
    #     # loc = input("Enter location: ")
    #     API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item_loc}'
    #     headers = {
    #         'Authorization': 'Bearer ' + access_token
    #     }
    #     response = requests.get(API_ENDPOINT, headers=headers)
        
    #     if response.status_code == 200:
    #         api_response = response.json()
    #         items = api_response.get('items', [])
    #         output=""
            
    #         for item_data in items:
    #             if item_data.get('item') == item_loc:
    #                 item_no = item_data.get('item')
    #                 location = item_data.get('location')
    #                 location_type = item_data.get('loctype')
    #                 price = item_data.get('price')
                    
    #                 output += f"item_no: {item_no}\n"
    #                 output += f"location: {location}\n"
    #                 output += f"location_type: {location_type}\n"
    #                 output += f"price: {price}\n\n"
            
    #         if output:
    #             return output
    #         else:
    #             print("error")
    #             return None
                
    # def get_api_response_usecase2(self, access_token, item2, loc2):
    #         self.item2 = item2
    #         self.loc2 = loc2
    #         # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL
    #         API_ENDPOINT = 'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&limit=10&item={self.item2}&location={self.loc2}'
    #         # Make the API request with the access token
    #         headers = {
    #             'Authorization': 'Bearer ' + access_token
    #         }
    #         response = requests.get(API_ENDPOINT, headers=headers)
    #         # Check the response status code
    #         if response.status_code == 200:
    #             api_response = response.json()
    #             items = api_response.get('items', [])
    #             output=""
    #             for item_data in items:
    #                 if (item_data.get('item') == self.item2 and item_data.get('location') == int(self.loc2)):
    #                     item_no=item_data.get('item')
    #                     location=item_data.get('location')
    #                     location_type=item_data.get('loctype')
    #                     price=item_data.get('price')
    #                     output += f"\nitem_no: {item_no}\n"
    #                     output += f"location: {location}\n"
    #                     output += f"location_type: {location_type}\n"
    #                     output += f"price: {price}\n\n"
    #                 # print(output)
    #                     return output
    #                 else:
    #                     # Error occurred
    #                     print('Error:', response.text)
    #                     return None
    # def get_api_response_usecase3(self, access_token, item3):
    #         self.item3 = item3
    #         # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL
    #         API_ENDPOINT = 'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item3}'
    #         # Make the API request with the access token
    #         headers = {
    #             'Authorization': 'Bearer ' + access_token
    #         }
    #         response = requests.get(API_ENDPOINT, headers=headers)
    #         # Check the response status code
    #         if response.status_code == 200:
    #             api_response = response.json()
    #             items = api_response.get('items', [])
    #             output=""
    #             for item_data in items:
    #                 if (item_data.get('item') == self.item3):
    #                     item_no=item_data.get('item')
    #                     # location=item_data.get('location')
    #                     # location_type=item_data.get('loctype')
    #                     price=item_data.get('price')
    #                     output += f"\nitem_no: {item_no}\n"
    #                     # output += f"location: {location}\n"
    #                     # output += f"location_type: {location_type}\n"
    #                     output += f"price: {price}\n\n"
    #                 # print(output)
    #                     return output
    #                 else:
    #                     # Error occurred
    #                     print('Error:', response.text)
    #                     return None