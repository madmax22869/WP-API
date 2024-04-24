import requests

def main():
    site_url = "https://wordpress-997378-4494710.cloudwaysapps.com"
    username = "max_api"
    password = "api_pass_123"

    auth_url = "https://wordpress-997378-4494710.cloudwaysapps.com/wp-json/salon/api/v1/login"
    auth_data = {
        "name": username,
        "password": password
    }

     # Create a requests.Request object to prepare the request
    print("Request URL with parameters:", auth_url + "?" + "&".join([f"{key}={value}" for key, value in auth_data.items()]))

    response = requests.get(auth_url + "?" + "&".join([f"{key}={value}" for key, value in auth_data.items()]))
    access_token = response.json().get("token")

    #print("access token:", access_token)

    print("Request URL:", auth_url)
    if response.status_code == 200:
        access_token = response.json().get("token")
        if access_token:
            print("Access token:", access_token)
        else:
            print("No access token found in the response.")
    else:
        print("Failed to authenticate. Status code:", response.status_code)
        print("Response content:", response.text)

    print("Welcome to the Wordpress API interaction menu!")
    print("1. Get all existing customers")
    print("2. Get existing user and add it to database")
    print("3. Update existing user")
    menu_choice = input("Select the function")

    if menu_choice == "1":
        get_all_customers()
    else:
        print("Invalid choice. Please enter 1 or 2.")

def get_all_customers():
    customers_url = "https://wordpress-997378-4494710.cloudwaysapps.com/wp-json/salon/api/v1/customers"

    response = requests.get(customers_url)

    if response.status_code == 200:
        customers = response.json()
        for customer in customers:
            print(f"Customer ID: {customer['id']}")
    else:
        print(f"Error fetching customers. Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    main()
