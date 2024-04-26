import requests
import json
import time
from pymongo import MongoClient

def main():

    site_url = "https://wordpress-997378-4494710.cloudwaysapps.com/wp-json/salon/api/v1/"
    username = "max_api"
    password = "api_pass_123"

    auth_data = {
        "name": username,
        "password": password
    }
    
    auth_url = site_url+"login?" + "&".join([f"{key}={value}" for key, value in auth_data.items()])

    print("Welcome to the Barber API synchroniser!")
    print("Service will synchronise all existing customers with service database each 60 seconds.")
    

     # Create a requests. Request a token to prepare operational requests.
    print("Request Token URL:", auth_url)

    response = requests.get(auth_url)

    print("please type update interval in seconds (number only)")
    time_interval = input()

    time_interval_int = int(time_interval)
 
    if response.status_code == 201:
        access_token = json.loads(response.text).get("access_token")
        if access_token:
            print("Access token:", access_token)
        else:
            print("No access token found in the response.")
    else:
        print("Failed to authenticate. Status code:", response.status_code)
        print("Response content:", response.text)

    while 0==0:
      customers_wp = get_customers_from_wp(access_token)
      customers_db = get_customers_from_db()
      synced_customers = sync_wp_to_db(customers_wp, customers_db)
      add_upd_customers(synced_customers['add_upd'])
      remove_customers(synced_customers['del'])
    
      time.sleep(time_interval_int)
    
    
def sync_wp_to_db(from_wp, from_db):
  #Analise raw lists of instances to produce lists of instances for insert/update and remove operations in database
  list_add_upd = []
  list_del = from_db
  
  for item_wp in from_wp:
    item_db = [obj for obj in from_db if obj['id'] == item_wp['id']]
    if item_db:
      list_add_upd.append(item_wp)  
      list_del.remove(item_db[0])
    else:
      list_add_upd.append(item_wp) 
  
  return {'add_upd':list_add_upd,'del':list_del}
  

def get_customers_from_wp(access_token):
  #Retrieve list of customers from Wordpress API with authorisation by retrieved Token
    customers_url = "https://wordpress-997378-4494710.cloudwaysapps.com/wp-json/salon/api/v1/customers"
    headers = {
    "Access-Token": access_token,
    "accept": "application/json"
}
    response = requests.get(customers_url,headers=headers)

    if response.status_code == 200:
        customers = response.json().get("items")
        return list(customers)
    else:
        print(f"Error fetching customers. Status code: {response.status_code}")
        print(response.json())

def get_customers_from_db():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://smaxim1970:smax150800@wp-api.p7vn9io.mongodb.net')
    db = client['wp_barber']
    customers_db = db['customers']

    return list(customers_db.find())

#Insert or update customers in database
def add_upd_customers(customers):
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://smaxim1970:smax150800@wp-api.p7vn9io.mongodb.net')
    db = client['wp_barber']
    customers_db = db['customers']
    inserted = 0
    
    #Process the list
    for record in customers:
      flt = {'id':record['id']}
      update = {'$set': record}
      #Update existing ones or insert new ones
      if customers_db.find_one_and_update(flt, update):
        continue
      customers_db.insert_one(record)
      inserted += 1
    print(f"Inserted {inserted}")
    print(f" Updated {len(customers)-inserted}")


#Remove customers from database
def remove_customers(customers):
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://smaxim1970:smax150800@wp-api.p7vn9io.mongodb.net')
    db = client['wp_barber']
    customers_db = db['customers']
    
    #Remove requested customers
    for record in customers:
      customers_db.delete_one(record)
    print(f" Removed {len(customers)}")


if __name__ == "__main__":
    main()


