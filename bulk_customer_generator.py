import json
import random
import string
from datetime import datetime, timedelta
import requests
import time
from faker import Faker

# Set up Faker
fake = Faker()
Faker.seed(12345)  # For reproducibility

# Constants for customer generation
LANGUAGES = ["English", "Spanish", "Hindi", "Mandarin", "Arabic", "French", "Russian", 
             "Portuguese", "Japanese", "German", "Korean", "Italian", "Dutch", "Swedish", 
             "Polish", "Vietnamese", "Turkish", "Thai", "Greek", "Romanian"]

GENDERS = ["Male", "Female", "Non-binary", "Prefer not to say"]

CONTACT_TYPES = ["Email", "Mobile", "Home Phone", "Work Phone", "WhatsApp", "Telegram", 
                "WeChat", "Line", "Viber", "Signal", "Skype", "Facebook", "LinkedIn"]

ID_TYPES = {
    "USA": ["Passport", "Driver's License", "Social Security Number", "State ID"],
    "India": ["Aadhaar Card", "PAN Card", "Voter ID", "Passport"],
    "UK": ["Passport", "Driving Licence", "National Insurance Number", "BRP"],
    "Canada": ["Passport", "Driver's License", "Social Insurance Number", "Health Card"],
    "Australia": ["Passport", "Driver's License", "Medicare Card", "Tax File Number"],
    "China": ["National ID", "Passport", "Hukou"],
    "Japan": ["My Number Card", "Passport", "Resident Card"],
    "Brazil": ["RG", "CPF", "Passport", "Work Card"],
    "Germany": ["Personal ID", "Passport", "Tax ID"],
    "France": ["National ID Card", "Passport", "Social Security Number"]
}

def random_date(start_year=1950, end_year=2005):
    """Generate a random date between start_year and end_year"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def random_future_date(start_year=datetime.now().year, years_ahead=10):
    """Generate a random date in the future"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(start_year + years_ahead, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def random_past_date(years_back=5):
    """Generate a random date in the past"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*years_back)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return (start_date + timedelta(days=random_number_of_days)).strftime("%Y-%m-%d")

def generate_id_value(id_type):
    """Generate a realistic looking ID value based on type"""
    if "Passport" in id_type:
        # Generate passport number like A12345678
        letter = random.choice(string.ascii_uppercase)
        numbers = ''.join(random.choices(string.digits, k=8))
        return f"{letter}{numbers}"
    elif "License" in id_type:
        # Generate driver's license like DL12345678
        return f"DL{''.join(random.choices(string.digits, k=8))}"
    elif "National ID" in id_type or "Personal ID" in id_type:
        # Generate national ID
        return ''.join(random.choices(string.digits, k=10))
    elif "Card" in id_type:
        # Generate card number
        return ''.join(random.choices(string.digits, k=12))
    elif "Number" in id_type:
        # Generate a number
        return ''.join(random.choices(string.digits, k=9))
    else:
        # Generic ID
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=6))
        return f"{letters}{numbers}"

def generate_customer():
    """Generate a random customer"""
    # Select a random country for more realistic data
    country = random.choice(list(ID_TYPES.keys()))
    
    # Generate address based on country
    if country == "USA":
        state = fake.state_abbr()
        city = fake.city()
        zip_code = fake.zipcode()
        address1 = fake.street_address()
        address2 = random.choice([fake.secondary_address(), ""])
    else:
        state = fake.state()
        city = fake.city()
        zip_code = fake.postcode()
        address1 = fake.street_address()
        address2 = random.choice([f"Apt {random.randint(1, 999)}", ""])
    
    # Generate name
    if random.random() < 0.7:  # 70% chance to have a middle name
        middle_name = fake.first_name()
    else:
        middle_name = ""
    
    # Generate contact details (1-3 contact methods)
    num_contacts = random.randint(1, 3)
    contact_types = random.sample(CONTACT_TYPES, num_contacts)
    contacts = []
    
    for contact_type in contact_types:
        if contact_type == "Email":
            value = fake.email()
        elif "Phone" in contact_type or contact_type in ["Mobile", "WhatsApp"]:
            value = fake.phone_number()
        else:
            value = fake.user_name()
        contacts.append({
            "type": contact_type,
            "value": value
        })
    
    # Generate identity proofs (1-2 documents)
    num_ids = random.randint(1, 2)
    id_types = random.sample(ID_TYPES[country], min(num_ids, len(ID_TYPES[country])))
    ids = []
    
    for id_type in id_types:
        issued_date = random_past_date(random.randint(1, 5))
        
        # Some IDs don't expire
        if id_type in ["Social Security Number", "PAN Card", "Tax ID", "National Insurance Number", "CPF"]:
            expiry_date = None
        else:
            expiry_date = random_future_date(datetime.now().year, random.randint(5, 10))
            
        ids.append({
            "type": id_type,
            "value": generate_id_value(id_type),
            "issuedDate": issued_date,
            "expiryDate": expiry_date
        })
    
    # Build the customer object
    customer = {
        "name": {
            "firstName": fake.first_name(),
            "middleName": middle_name,
            "lastName": fake.last_name()
        },
        "dateOfBirth": random_date(1960, 2000),
        "gender": random.choice(GENDERS),
        "language": random.choice(LANGUAGES),
        "contactDetails": contacts,
        "address": {
            "addressLine1": address1,
            "addressLine2": address2,
            "city": city,
            "state": state,
            "country": country,
            "zipCode": zip_code
        },
        "identityProofs": ids
    }
    
    return customer

def generate_and_save_customers(num_customers, output_dir="./customers"):
    """Generate customers and save to JSON files"""
    import os
    
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    customers = []
    for i in range(num_customers):
        customer = generate_customer()
        customers.append(customer)
        
        # Save individual customer file
        with open(f"{output_dir}/customer_{i+1}.json", "w") as f:
            json.dump(customer, f, indent=2)
    
    return customers

def post_customers_to_api(customers, api_url, batch_size=10):
    """Post customers to API endpoint"""
    success_count = 0
    failed_count = 0
    
    for i, customer in enumerate(customers):
        try:
            response = requests.post(api_url, json=customer)
            
            if response.status_code in [200, 201]:
                print(f"Customer {i+1} successfully added, status: {response.status_code}")
                success_count += 1
            else:
                print(f"Failed to add customer {i+1}, status: {response.status_code}, message: {response.text}")
                failed_count += 1
                
            
            # Print status after each batch
            if (i + 1) % batch_size == 0:
                print(f"Progress: {i+1}/{len(customers)} customers processed")
                
        except Exception as e:
            print(f"Error posting customer {i+1}: {str(e)}")
            failed_count += 1
    
    print(f"\nSummary: {success_count} customers successfully added, {failed_count} failed")

if __name__ == "__main__":
    # Configuration
    NUM_CUSTOMERS = 10000  # Change this to generate more or fewer customers
    API_URL = "http://localhost:8080/api/customer"  # Change this to your actual API endpoint
    
    # Generate and save customer data
    print(f"Generating {NUM_CUSTOMERS} customers...")
    customers = generate_and_save_customers(NUM_CUSTOMERS)
    print(f"Generated and saved {NUM_CUSTOMERS} customer files to ./customers/ directory")
    
    # Ask if user wants to post to API
    post_to_api = input("Do you want to post these customers to the API? (y/n): ")
    if post_to_api.lower() == 'y':
        print(f"Posting customers to {API_URL}...")
        post_customers_to_api(customers, API_URL)
    else:
        print("Customers were generated but not posted to the API.")