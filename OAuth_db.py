import requests

class Oauth:
    def __init__(self, client_id, client_secret, access_token_url, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_url = access_token_url
        self.scope = scope

    def generate_token(self):

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        response = requests.post(self.access_token_url, headers=headers, data=data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print('Error generating in access token:', response.text)
            return None

client_id = 'FTS_CLIENT_APPID'
client_secret = '6057adc8-7d62-4495-a11c-bb29eb09f4b6'
access_token_url = 'https://idcs-7e6742312d274583aa0f703733016616.identity.oraclecloud.com/oauth2/v1/token'
scope = 'rgbu:merch:MFCS-STG1'
oauth_token = Oauth(client_id, client_secret,access_token_url, scope)
access_token = oauth_token.generate_token()
    # print(access_token)
if access_token:

        # print('Access token:', access_token)

    def get_api_response(access_token):
        item = input("Enter item no: ")
        # loc = input("Enter location: ")
        API_ENDPOINT = 'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={item}'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        
        if response.status_code == 200:
            api_response = response.json()
            items = api_response.get('items', [])
            output=""
            
            for item_data in items:
                if item_data.get('item') == item:
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
                return "Item not found"
        
        return "Error"

out = get_api_response(access_token)
print(out)
            
#             for item_data in items:
#                 # print("item:", item)
#                 # print("item_data['item']:", item_data.get('item'))
#                 # print("new")
#                 if item_data.get('item') == item:
#                     item_no=item_data.get('item')
#                     # 100060021
#                     location=item_data.get('location')
#                     # 11003
#                     location_type=item_data.get('loctype')
#                     price=item_data.get('price')
#                     output += f"item_no: {item_no}\nlocation: {location}\nlocation_type: {location_type}\nprice: {price}"
#                     # output += f"item_no: {item_no}\nlocation: {location}\nprice: {price}"
                    
#                     return output
#             else:
#                 print('Error') 
#                 return "item not found"
# out = get_api_response(access_token)
# print(out)
