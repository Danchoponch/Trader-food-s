# Trader food's

## Project Overview
This project combines **API integration**, **web scraping**, and **data cleaning** techniques to create a unique, clean dataset with **real-world value**. The pipeline gathers data from:

1. **API**: The Spoonacular API, which provides information on recipes, ingredients, and nutritional content.
2. **Web Scraper**: Trader Joe's website, specifically scraping product details including price, weight, and nutritional information (fat, carbohydrates, protein). Trader Joe’s doesn’t have a publicly available API, which makes web scraping necessary.

The combination of these data sources allows us to generate a comprehensive dataset, matching ingredients from recipes with available product data from Trader Joe's, which can be useful for meal planning, grocery shopping, and nutritional analysis.

## Data Description
### API Data (Spoonacular)
- **Recipes**: Extracted recipe details, including the title, ID, and ingredients.
- **Ingredients**: For each selected recipe, the API provides a detailed list of ingredients, including their names and amounts.

### Scraped Data (Trader Joe's)
- **Products**: Product names, prices, volume/weight, and detailed nutritional information are scraped. This includes data like calories, fat, carbs, and protein.
  
By combining the two, we enable users to match recipe ingredients to real-world products they can buy from Trader Joe’s, along with their price and nutritional content.

## Value Proposition
This dataset serves as a **grocery meal planner** and **cost estimator** with an additional focus on **nutrition**. With this pipeline, users can:
1. **Find the cost and nutritional information** of their favorite recipes using actual product data from a retailer.
2. **Save time and effort** in meal planning by knowing which products are suitable for specific recipes.
3. **Customize recipes** based on availability or cost of ingredients, using Trader Joe’s products.


## Current Algorithm Limitations
The current algorithm for matching ingredients with products is not optimal and needs improvement. Some potential enhancements include:
- **Improved Matching Logic**: Implementing more sophisticated matching algorithms, such as fuzzy matching, to better account for variations in ingredient names (e.g., "sugar" vs. "granulated sugar").
- **Nutritional Value Comparison**: Adding a layer to compare the nutritional values of ingredients with products to suggest healthier alternatives.
- **User Customization**: Allowing users to specify dietary restrictions or preferences to refine product recommendations further.

## How the Application Works
1. **User Input**: You input the name of a meal or recipe you want to cook.
2. **Meal Selection**: Choose from a list of options that the application provides based on your input.
3. **Ingredient Lookup**: The program looks at the ingredients needed for your selected meal and searches in the scraped database.
4. **Output**: Relevant products from Trader Joe's that match the ingredients are displayed, along with their prices and nutritional information. The final output dataset is matched_products.csv

## Scraping Code and Data Storage
In `main.py`, the code for scraping is commented out because it takes a long time to execute. The scraped data is stored in the `out.csv` file, which is utilized for matching with recipe ingredients during the execution of the application.

## How to Run

### Prerequisites
Make sure you have Python installed, along with the necessary libraries. You can install them by running:

```bash
pip install -r requirements.txt
```

Add your key to a .env file in the following format:

```bash
API_KEY=your_spoonacular_api_key
```

Run program
```bash
python main.py
```



### Final Notes
- **Data Accuracy**: Keep in mind that grocery prices and product availability fluctuate, so this dataset represents a snapshot at the time of scraping.
