import re,requests
import pandas as pd
import shutil
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet,FollowupAction, ActionExecuted
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import os, PyPDF2
import yaml
from .trydb import jsonConversion, allFunc
# from rasa.shared.nlu.training_data.readers.markdown_reader import MarkdownReader
# # from bardapi import bard
# # import bardapi.core
# import logging
class CustomAction(Action):
    def name(self) -> Text:
        return "custom_action"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve information from the conversation
        # user_value = tracker.latest_message("text")
        user_value = tracker.latest_message['text']
        #incase if the sentence is stored completely, extract the number
        number = re.search(r'\d+', user_value).group()
        # Set the value of a slot using the reusable function
        return [SlotSet("item", number),SlotSet("item_value", number)]
    
class CustomAction1(Action):
    def name(self) -> Text:
        return "custom_action_for_loc"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve information from the conversation
        # user_value = tracker.latest_message("text")
        item_value=tracker.get_slot("item_value")
        print(item_value)
        user_value = tracker.latest_message['text']
        print(user_value)
        #incase if the sentence is stored completely, extract the number
        number = re.search(r'\d+', user_value).group()
        print()
        # Set the value of a slot using the reusable function
        return [SlotSet("loc", number), SlotSet("item", item_value)]
    
class ItemDetailsOauthApi(Action):
    def name(self) -> Text:
        return "action_all_item_prices"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message("inside the item function")
        client_id = 'FTS_CLIENT_APPID'
        client_secret = '6057adc8-7d62-4495-a11c-bb29eb09f4b6'
        access_token_url = 'https://idcs-7e6742312d274583aa0f703733016616.identity.oraclecloud.com/oauth2/v1/token'
        scope = 'rgbu:merch:MFCS-STG1'
        oauth_token = jsonConversion(client_id, client_secret,access_token_url, scope)
        access_token = oauth_token.generate_token()
        if access_token:
            allItemPrices = oauth_token.get_api_response_usecase1(access_token)
            out=str(allItemPrices)
            print(out)
            dispatcher.utter_message(text=out)
        # # Sample data
        # item_data = [
        #     {"item_no": "100190308", "location": "102", "location_type": "S", "price": "1025"},
        #     {"item_no": "100185305", "location": "105", "location_type": "S", "price": "19266.69"},
        #     {"item_no": "100035000", "location": "607", "location_type": "S", "price": "275.25"}
        # ]
 
        # if item_data:
        #     df = pd.DataFrame(item_data)
        #     filename = "output.xlsx"
        #     df.to_excel(filename, index=False)
        #     dispatcher.utter_message(text="Here is the output file.")
 
        #     # Get the file path relative to the project directory
        #     file_path = os.path.join(os.getcwd(), filename)
 
        #     # Get the user's "Downloads" directory path
        #     downloads_path = os.path.expanduser("~\\Downloads")
 
        #     # Move the file to the user's "Downloads" directory
        #     new_file_path = os.path.join(downloads_path, filename)
        #     shutil.move(file_path, new_file_path)
 
        #     # Create the URL to the file in the user's "Downloads" directory
        #     file_url = f"file://{new_file_path}"
 
        # # buttons = [
        #     #     {
        #     #         "title": "Download the file",
        #     #         "payload": file_url
        #     #     }
        #     # ]
 
        #     dispatcher.utter_message(
        #         text=f"Click [here]({file_url}) to download the file.",
        #         attachment={
        #             "name": filename,
        #             "data": file_url
        #         }
        #     )
        # else:
        #     dispatcher.utter_message(text="No item prices found.")
        return[]
    
class Itemdetails(Action):
    def name(self)-> Text:
        return "action_get_pricedetail"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        item =tracker.get_slot('item')
        loc = tracker.get_slot('loc')
       
        client_id = 'FTS_CLIENT_APPID'
        client_secret = '6057adc8-7d62-4495-a11c-bb29eb09f4b6'
        access_token_url = 'https://idcs-7e6742312d274583aa0f703733016616.identity.oraclecloud.com/oauth2/v1/token'
        scope = 'rgbu:merch:MFCS-STG1'
        oauth_token = jsonConversion(client_id, client_secret,access_token_url, scope)
        token= oauth_token.generate_token()
        if token:
            get_price_detail=oauth_token.get_api_response(token,item,loc) 
            if get_price_detail == None:
                print("inside action else part")
                dispatcher.utter_message("Seems like, the item is not present in the mentioned location.\n you can try checking if the entered values are correct. \n you can also try searching for different values.")
            dispatcher.utter_message(get_price_detail)
            #error message is also returned from the file. So  both are pprinted through the if statement.
        return [SlotSet('item', None), SlotSet('loc', None), SlotSet('item_prev', item), SlotSet('item_value_prev', loc), SlotSet('uc2_output', get_price_detail)]
class GetPriceatAllLocation(Action):
    def name(self)-> Text:
        return "action_getPrice_at_All_Location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        item_loc = tracker.latest_message['text']
        item= tracker.get_slot("item")
        print(item_loc+item)
        client_id = 'FTS_CLIENT_APPID'
        client_secret = '6057adc8-7d62-4495-a11c-bb29eb09f4b6'
        access_token_url = 'https://idcs-7e6742312d274583aa0f703733016616.identity.oraclecloud.com/oauth2/v1/token'
        scope = 'rgbu:merch:MFCS-STG1'
        oauth_token = jsonConversion(client_id, client_secret,access_token_url, scope)
        access_token = oauth_token.generate_token()
        if access_token:
            allItemPrices = oauth_token.get_api_response_usecase3(access_token,item_loc)
            # out=str(allItemPrices)
            print(allItemPrices)
            dispatcher.utter_message(text=allItemPrices)
            #error message is also returned from the file. So  both are pprinted through the if statement.
        return[SlotSet('item_value', item_loc),SlotSet('item_loc', item_loc), SlotSet('uc3_output', allItemPrices)]
#whenever the user repeats the 2nd usecase again, since the slots are already filled, it is taking the previous location value automatically
#and giving the wrong output. instead, ask prompt the user if they want details for the same location, if not, null the slots and run.
class CustomActionUtterRepeat(Action):
    def name(self) -> Text:
        return "action_utter_display_prev_item"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        item_prev = tracker.get_slot('item_prev')
        item_value_prev = tracker.get_slot('item_value_prev')
        specific_output = tracker.get_slot('uc2_output')
        print(f"specific output {specific_output}")
        
        if specific_output == None and item_prev:
            dispatcher.utter_message(f"Earlier you have checked details for the item {item_prev} at the location {item_value_prev} and looks like there was no data present or there could have been an error in the data that was entered..")
        elif item_prev and item_value_prev or specific_output:
            dispatcher.utter_message(f"Earlier you have checked details for the item {item_prev} at the location {item_value_prev}.\n And the details related to your previous search was \n{specific_output}")
            dispatcher.utter_message("If you want to check for a different item, or to check for different locations,")
        else:
            print("the values are none. story continues..")
        return []
    
class CustomActionUtterRepeatUc3(Action):
    def name(self) -> Text:
        return "action_utter_display_prev_item_uc3"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        item_value = tracker.get_slot('item_loc')
        uc3_output = tracker.get_slot('uc3_output')
        #if condition for the 3rd usecase - item at all lcoation
        if item_value:
            dispatcher.utter_message(f"Earlier you have checked details for the item {item_value}.\n Here is the price details of the item {item_value} at all location.\n {uc3_output}")
            dispatcher.utter_message("If you want to check for a different item's detail, feel free to, ")
        else:
            print("the values are none. story continues..")
        return []     
#-------------------------------------------STAGE 2 ------------------------------------------------------------------------------
#keeping the a"action_default_fallback" and "action_test_fallback" as it is, as, if suppose domain or nlu fallback gets hit directly, these two will work
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        # user_input = tracker.get_slot("user_input_question")
        user_input=tracker.latest_message.get("text")
        print(user_input)
        # user_messages = [event['text'] for event in tracker.events if event['event'] == 'user']
        # user_input = user_messages[-2] if len(user_messages) >= 2 else None  

       
        if user_input:
            # user_input = user_message[-1]
            # print (user_input)
            object=allFunc()
            response = object.call_chatgpt_api(user_input)
            dispatcher.utter_message(response)
        return[SlotSet("user_input_question", None)]

class ActionTestFallback(Action):
    def name(self) -> Text:
        return "action_test_fallback"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        #when coming from the check_intent action
        error_text = "I apologize for the inconvenience, but it looks like the information that you are trying to get is not retail specific.\n\
                    You can ask me anything related the domain, I will do my best to help you in any way that I can."
        # user_input=tracker.get_slot("user_input_question")
        print(error_text, end=" ")
        # dispatcher.utter_message(text=error_text)
        dispatcher.utter_message()

        return[SlotSet("user_input_question", None)]

#user_input_question entity is not used, as entity was only used to check only the condition.
#taking the latest message from the user only will work fine, if the functions are redirected in this action.
#(redirection step is added - but since it didn't work, adding the steps from the two functios again directly here)
#THIS ACTION IS TRIGGERED WHENEVER THE USER ENTERS A STATEMENT AND NON RETAIL SPECIFIC WORDS
class CheckKeywordAction(Action):
    def name(self) -> Text:
        return "check_value_in_intent"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # keyword=tracker.get_slot("user_input_question")
        keyword=tracker.latest_message.get("text")
        print(f"before: {keyword}")

        #the extracted output is like this, - keywoed [{'event': 'slot', 'timestamp': None, 'name': 'user_input_question', 'value': 'zone'}]. so take the value again from the list
        # keyword = keyword[0]['value'] - use this step if the entity values is taken

        # Load the NLU training data
        nlu_data = self.load_nlu_data()

        #the nlu data has nlu file data in json format. 
        #this part access the domain details examples from the json data and it is stored in examples
        for intent_data in nlu_data:
            if "nlu" in nlu_data:
                for intent_data in nlu_data["nlu"]:
                    if isinstance(intent_data, dict) and intent_data.get("intent") == "domain_details":
                        examples_str = intent_data.get("examples", "")
                        examples = examples_str.split("\n")
                        print(f"exstr: {examples}")
                        #   # Remove hyphens from the examples
                        examples = [example.replace("- ", "") for example in examples]
                        print(keyword)
                        print(examples)      
                        #calling the check_words function here.                  
                        result = self.check_words_in_intent(keyword, examples)
                        print(result)  # True/False

                        if result == True:
                            object=allFunc()
                            #since retail specific definition is needed, adding it in the user entered sentence
                            keyword=keyword + "- in retail"
                            response = object.call_chatgpt_api(keyword)
                            dispatcher.utter_message(response)
                            return [ActionExecuted("action_default_fallback")]
                        else:
                            error_text = "I apologize for the inconvenience, but it looks like the information that you are trying to get is not retail specific.\n\
                                You can ask me anything related the domain, I will do my best to help you in any way that I can."
                    # user_input=tracker.get_slot("user_input_question")
                            dispatcher.utter_message(text=error_text)
                            return [SlotSet("user_input_question", None)]

    def load_nlu_data(self):
        # Load the NLU training data from the nlu.yml file
        nlu_file_path=r"C:\\Users\\yraja\\LogicBot\\rasa\\data\\nlu.yml"
        with open(nlu_file_path, "r") as file:
            return yaml.safe_load(file)
    def check_words_in_intent(self, user_input, intent_examples):
        # Convert user input to lowercase
        user_input = user_input.lower()
        # Convert intent examples to lowercase and remove empty strings
        intent_examples = [example.lower() for example in intent_examples if example]
        # Split user input into individual words
        user_words = user_input.split()
        # List to store matched words and their positions

        matched_words = []
        # Check if any word matches the intent examples
        for word in user_words:
            #IMPORTANT - adding this regex to take the word as a whole, not a part of the word.("wholesale" should not get matched with "who")
            regex = r"\b" + re.escape(word) + r"\b"
            for i, example in enumerate(intent_examples):
                if re.search(regex, example):
                    matched_words.append((word, i))
#matched words tells which word in the array is matched - useful for debugging - NOT NECESSARY TO RETURN AND USE
        if matched_words:
            print("Match found! Matched words:")
            for word, position in matched_words:
                print(f"Word: {word}, Position: {position}")
            return True
        else:
            return False

                
# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet
# class ReadIntentsAction(Action):
#     def name(self):
#         return "check_value_in_intent"
#     def run(self, dispatcher, tracker, domain):
#         self.set_the_slot(tracker)
#         keyword=tracker.get_slot("user_input_question")
#         # Read the NLU data from the domain file
#         nlu_data = domain.get('intents', [])
#         # Find the "domain_details" intent
#         domain_details_intent = None
#         # for intent in nlu_data:
#         #     if intent.get('name') == 'domain_details':
#         #         domain_details_intent = intent
#         #         break
#         # Read the NLU data from the domain file
#         nlu_data = domain.get('intents', [])
#         # Find the "domain_details" intent
#         domain_details_intent = next(
#             (intent for intent in nlu_data if intent.get('name') == 'domain_details'),
#             None
#         )
#         if domain_details_intent:
#             # Extract the words from the "domain_details" intent examples
#             examples = domain_details_intent.get('examples', [])
#             words = set()
#             for example in examples:
#                 words.update(example.split())
#             if keyword in words:
#                 print("exist")
#             # Set a slot with the words for further use
#             return [FollowupAction(ActionDefaultFallback)]
#         else:
#             print(f"inside else part: {keyword}")
#             dispatcher.utter_message("I apologize for the inconvenience, but it looks like the information that you are trying to get is not retail specific.\n")
#             dispatcher.utter_message("You can ask me anything related the domain, I will do my best to help you in any way that I can.")
#             return [SlotSet("user_input_question", None)]
    
#     def set_the_slot(self, tracker: Tracker) -> List[Dict[Text, Any]]:
#         entity_value = next(tracker.get_latest_entity_values("user_input_question"), None)
#         print(f"entity value {entity_value}")
#         return [SlotSet("user_input_question", entity_value)]
        
