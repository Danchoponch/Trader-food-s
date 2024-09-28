import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sys
from prettytable import PrettyTable

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")


# Uncomment code below if you wish to see the process of scraping data.
# It is commented out because scraping takes >8 minutes.
# All scraped data is stored in the csv file in this directory.

# # Initialize a Chrome WebDriver instance to interact with the website
# driver = webdriver.Chrome()

# driver.get("https://www.traderjoes.com/home/products/category/food-8")

# time.sleep(2)  # Pause to allow the page to load

# # List to store product data scraped from the website
# product_data = []
# count = 20  # Number of pages to scrape
# pattern = re.compile(r'\/home\/products\/pdp\/[a-zA-Z0-9\-]+\-\d+')  # Regular expression to match product links

# # Function to scrape data from the current page's product links
# def scrape_current_page(links):
#     for link in links:
#         driver.get(f"https://www.traderjoes.com{link}")
#         time.sleep(3)  # Pause to allow the page to load
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
        
#         # Extract product details
#         product_name = soup.find("h1", attrs={"class": "ProductDetails_main__title__14Cnm"})
#         product_price = soup.find("span", attrs={"class": "ProductPrice_productPrice__price__3-50j"})
#         product_unit = soup.find("span", attrs={"class": "ProductPrice_productPrice__unit__2jvkA"})
#         product_unit = product_unit.text[1:] if product_unit else None
#         product_calories = soup.find_all("div", attrs={"class": "Item_characteristics__text__dcfEC"})
#         product_table = soup.find("table", attrs={"class": "Item_table__2PMbE"})

#         # Create a dictionary to hold the product's data
#         product_obj = {
#             "Name": product_name.text if product_name else None,
#             "Price": product_price.text if product_price else None,
#             "Total_volume": product_unit,
#             "Calories": product_calories[1].text if product_calories else None
#         }

#         # If the product has a nutritional table, extract its details
#         if(product_table):
#             tbody = product_table.find("tbody", attrs={"class": "Item_table__body__32J7y"})

#             for row in tbody.find_all("tr", class_="Item_table__row__3Wdx2"):
#                 td_tags = row.find_all("td", class_="Item_table__cell__aUMvf")

#                 # Extract the name (1st td) and amount (2nd td) from the table rows
#                 if len(td_tags) >= 2:
#                     parameter_name = td_tags[0].text.strip()
#                     parameter_amount = td_tags[1].text.strip()
#                     product_obj[parameter_name] = parameter_amount  # Store the parameter

#         # Add the product data to the list
#         product_data.append(product_obj)
#         driver.back()

#     return 0


# # Function to navigate to the next page of products
# def go_to_next_page():
#     try:
#         next_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "Pagination_pagination__arrow_side_right__9YUGr"))
#         )
#         # Use JavaScript to click the button
#         driver.execute_script("arguments[0].click();", next_button)
#         return True  # Success, moved to the next page
#     except Exception as e:
#         print(f"Failed to click next button: {e}")
#         return False  # Failed to move to the next page

    
# while (count > 0):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # Find all product links on the current page
#     product_tags = soup.find_all("a", attrs={"class": 'ProductCard_card__img_link__2bBqA'})
#     product_links = []

#     for tag in product_tags:
#         href = tag['href']
#         match = pattern.search(href)
#         if match:
#             product_links.append(match.group())
    
#     # Scrape data from the product links
#     scrape_current_page(product_links)

#     time.sleep(3)

#     # Navigate to the next page
#     success = go_to_next_page()
#     if not success:
#         break 

#     count -= 1  # Decrease the page count
#     time.sleep(2)


# # Save the scraped product data to a CSV file
# df = pd.DataFrame(product_data)
# df.to_csv('out.csv', index=False)  


# The following code works with an existing database that was previously scraped.
# You could temporarily comment out the above code to scrape first.
df_meal = pd.read_csv("out.csv")  # Load the previously scraped product data from CSV

# Prompt the user for the meal they want to eat
meal = input("Please enter a meal that you would want to eat\n")

# Spoonacular API for searching meal recipes
url_meals = "https://api.spoonacular.com/recipes/complexSearch"

headers ={
    "x-api-key": API_KEY
}

# API query parameters to search for the meal
params_meals = {
    "query": meal,
    "number": 5  # Limit the results to 5 meals
}

# Try-except block to handle any potential errors
try:
    # Make a GET request to the Spoonacular API
    response_meal = requests.get(url=url_meals, headers=headers, params=params_meals)
    meals = response_meal.json()['results']  # Parse the results

    meal_names = []  # List to store meal names
    for obj in meals:
        meal_names.append(obj['title'])
        print(obj['title'])  # Print each meal name
    
    if meal_names == []:  # If no meals are found
        print("Sorry, no such meals/dishes")
        sys.exit()  # Exit the application


    print()
    meal_select = ""

    # Prompt user to select one of the meals found
    while (True):
        meal_select = input("Please select a meal that you would like to make\n")
        if(meal_select in meal_names):
            break
        

    # Retrieve the selected meal's ID
    meal_select_id = 0
    for obj in meals:
        if obj['title'] == meal_select:
            meal_select_id  = obj['id']
            break
    
    meal_select_id = str(meal_select_id).strip()  # Clean up the ID

    # Get detailed information about the selected meal
    response_ingredients = requests.get(f"https://api.spoonacular.com/recipes/{meal_select_id}/information", headers=headers)

    ingredients = response_ingredients.json()['extendedIngredients']  # Get the list of ingredients

    ingredients_names = []
    for obj in ingredients:
        ingredients_names.append(obj['name'])  # Extract ingredient names

    # Search for matching products from the previously scraped data based on ingredients
    matches = df_meal[df_meal['Name'].str.contains('|'.join(ingredients_names), case=False, na=False)]
    matches.to_csv('matched_products.csv', index=False)  # Save the matched products to a CSV file

    # Initialize a PrettyTable to display the matched products
    table = PrettyTable()

    table.field_names = matches.columns  # Set column headers

    # Add rows to the table
    for row in matches.itertuples(index=False):
        table.add_row(row)

    print(table)  # Display the table of matched products

# Handle errors during the API request
except:
    print("Sorry, couldn't find such meal")
