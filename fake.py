import csv
from faker import Faker
import random

# Initialize the Faker object
fake = Faker()

# Define a list of electronic product names and categories
product_names = [
    "Smartphone", "Laptop", "Tablet", "Smartwatch", "Bluetooth Speaker",
    "Gaming Console", "Smart TV", "Digital Camera", "Drone", "Portable Charger",
    "Router", "Headphones","Projector", "Printer", "Monitor", "Keyboard", "Mouse", "Webcam"
]

categories = ["Mobile Phones", "Computers", "Audio", "Wearable Tech", "Gaming", "Home Entertainment", "Camera", "Accessories"]

# Define the number of records to generate
num_records = 50

# Create a CSV file and write the header
with open("data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["product_id", "product_name", "category", "price", "quantity_sold", "rating", "review_count"])

    # Generate fake data for each product
    for _ in range(num_records):
        product_id = fake.uuid4()[0:4]           
        product_name = random.choice(product_names)
        category = random.choice(categories)
        price = random.randint(20, 2000)       
        quantity_sold = random.randint(10, 1000) 
        rating = random.randint(1, 5)            
        review_count = random.randint(1, 5000)   

        # Write the row to the CSV file
        writer.writerow([product_id, product_name, category, price, quantity_sold, rating, review_count])

print("Data generation complete. Check the 'electronic_products.csv' file.")
