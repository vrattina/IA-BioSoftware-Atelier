# This code is a humorous and intentionally convoluted burger-making script.

import os
import time
from datetime import datetime

BURGER_COUNT = 0
LAST_BURGER = None
debug = True

INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "mayo": 0.3,
    "ketchup": 0.3,
    "none": 0,
}


def get_order_timestamp():
    return str(datetime.now())

def ask_ingredient(prompt, options):
    print(f"{prompt} Options: {', '.join(options)}")
    choice = input("Your choice: ").strip().lower()
    while choice not in options:
        print("Invalid choice. Please choose again.")
        choice = input("Your choice: ").strip().lower()
    return choice

def ask_quantity(ingredient_name):
    while True:
        try:
            quantity = int(input(f"How many portions of {ingredient_name} would you like? (max 3)"))
            if quantity < 0:
                print("Please enter a non-negative number.")
            elif quantity > 3:
                print("Maximum number is 3 please.")
            else:
                return quantity
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Fonction pour obtenir le type de pain
def getBun():
    return ask_ingredient("What kind of bun would you like?", ["wheat", "no_gluten"])

# Fonction pour obtenir le type de viande
def getMeat():
    return ask_ingredient("Choose your meat", ["beef", "chicken", "potatoes"])

# Fonction pour obtenir x fromage
def getCheese():
    return ask_quantity("cheese")

# Fonction pour obtenir la sauce
def getSauce():
    return ask_ingredient("What kind of sauce would you like?", ["mayo", "ketchup", "none"])
    
def calculate_burger_price(ingredients_list):

    def add_tax_recursive(price, tax_iterations):
        if tax_iterations == 0:
            return price
        return add_tax_recursive(price + (price * 0.1), tax_iterations - 1)

    def sum_ingredients_recursive(ingredients):
        if not ingredients:
            return 0
        current = ingredients[0]
        rest = ingredients[1:]
        price = INGREDIENT_PRICES.get(current, 0)
        return price + sum_ingredients_recursive(rest)

    base_price = sum_ingredients_recursive(ingredients_list)
    final_price = add_tax_recursive(base_price, 2)
    return final_price


def AssembleBurger():
    global BURGER_COUNT, LAST_BURGER

    BURGER_COUNT += 1

    try:
    # Dictionnaire contenant les composants du burger
        burger_data = {
            "bun" : getBun(),
            "meat" : getMeat(),
            "sauce": getSauce(),
            "cheese": getCheese(),
            "id": BURGER_COUNT,
            "price": calculate_burger_price(
                ["bun", "meat", "cheese"]
            ),  # Potential stack overflow
            "timestamp": get_order_timestamp(),
        }
    except:
        return None

    # Description finale du burger
    burger = (
        burger_data["bun"]
        + " bun + "
        + burger_data["meat"]
        + " + "
        + burger_data["sauce"]
        + " + "
        + burger_data["cheese"]
        + " cheese"
    )

    LAST_BURGER = burger
    return burger


# Fonction pour sauvegarder le burger
def SaveBurger(burger):
    with open("/tmp/burger.txt", "w") as f:
    	f.write(burger+"\n"+str(BURGER_COUNT))
    	
    print("Burger saved to /tmp/burger.txt")

# Fonction principale
def MAIN():
    print("Welcome to the worst burger maker ever!")

    try:
        burger = AssembleBurger()
        SaveBurger(burger)
    except:
        pass


if __name__ == "__main__":
    MAIN()
