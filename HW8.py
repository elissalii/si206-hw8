# Your name: Elissa Li
# Your student id: 3814 5408
# Your email: elissali@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    # create a connection to the database file
    conn = sqlite3.connect(db)
    
    # create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # execute a SELECT query to get all the restaurant data
    cursor.execute("SELECT name, category, building, rating FROM restaurants")
    
    # fetch all the results and store them in a list of tuples
    results = cursor.fetchall()
    
    # create a nested dictionary to store the restaurant data
    rest_data = {}
    
    # iterate over the results and add them to the dictionary
    for result in results:
        name = result[0]
        category = result[1]
        building = result[2]
        rating = result[3]
        
        rest_data[name] = {
            "category": category,
            "building": building,
            "rating": rating
        }
    
    # close the cursor and connection
    cursor.close()
    conn.close()
    
    return rest_data

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    # create a connection to the database file
    conn = sqlite3.connect(db)
    
    # create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # execute a SELECT query to get the count of restaurants in each category
    cursor.execute("SELECT category, COUNT(*) FROM restaurants GROUP BY category")
    
    # fetch all the results and store them in a dictionary
    results = cursor.fetchall()
    
    rest_categories = {}
    
    # iterate over the results and add them to the dictionary
    for result in results:
        category = result[0]
        count = result[1]
        
        rest_categories[category] = count
    
    # create a bar chart
    plt.bar(rest_categories.keys(), rest_categories.values())
    plt.title("Restaurant Categories")
    plt.xlabel("Category")
    plt.ylabel("Number of Restaurants")
    plt.show()
    
    # close the cursor and connection
    cursor.close()
    conn.close()
    
    return rest_categories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    # Find highest-rated restaurant category and its average rating
    cur.execute('''SELECT category, AVG(rating) AS avg_rating
                   FROM restaurants
                   GROUP BY category
                   ORDER BY avg_rating DESC
                   LIMIT 1''')
    highest_category = cur.fetchone()

    # Find building with highest-rated restaurants and its average rating
    cur.execute('''SELECT building, AVG(rating) AS avg_rating
                   FROM restaurants
                   GROUP BY building
                   ORDER BY avg_rating DESC
                   LIMIT 1''')
    highest_building = cur.fetchone()

    conn.close()

    # Create bar charts
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Bar chart of categories and their ratings
    cur.execute('''SELECT category, AVG(rating) AS avg_rating
                   FROM restaurants
                   GROUP BY category
                   ORDER BY avg_rating DESC''')
    categories = [row[0] for row in cur.fetchall()]
    ratings = [row[1] for row in cur.fetchall()]
    ax1.bar(categories, ratings)
    ax1.set_xticklabels(categories, rotation=45)
    ax1.set_ylabel('Average Rating')
    ax1.set_title('Highest-Rated Restaurant Categories')

    # Bar chart of buildings and their ratings
    cur.execute('''SELECT building, AVG(rating) AS avg_rating
                   FROM restaurants
                   GROUP BY building
                   ORDER BY avg_rating DESC''')
    buildings = [row[0] for row in cur.fetchall()]
    ratings = [row[1] for row in cur.fetchall()]
    ax2.bar(buildings, ratings)
    ax2.set_xticklabels(buildings, rotation=45)
    ax2.set_ylabel('Average Rating')
    ax2.set_title('Highest-Rated Buildings')

    plt.tight_layout()
    plt.show()

    return [highest_category, highest_building]

#Try calling your functions here
def main():
    db = 'restaurants.db'

    # Load restaurant data
    rest_data = load_rest_data(db)

    # Plot restaurant categories
    rest_categories = plot_rest_categories(db)

    # Find restaurants in building
    building_num = 123
    rest_in_building = find_rest_in_building(building_num, db)

    # Get highest rating information and plot bar charts
    highest_rating = get_highest_rating(db)

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
