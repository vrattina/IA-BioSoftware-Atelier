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
            quantity = int(input(f"How many portions of {ingredient_name} would you like? (max 3) "))
            if quantity < 0:
                print("Please enter a non-negative number.")
            elif quantity > 3:
                print("Maximum number is 3 please.")
            else:
                return quantity
        except ValueError:
            print("Invalid input. Please enter an integer.")

def getBun():
    return ask_ingredient("What kind of bun would you like?", ["wheat", "no_gluten"])

def getMeat():
    return ask_ingredient("Choose your meat", ["beef", "chicken", "potatoes"])

def getCheese():
    return ask_quantity("cheese")

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
        bun = getBun()
        meat = getMeat()
        sauce = getSauce()
        cheese_qty = getCheese()

        ingredients = [bun, meat, sauce] + ["cheese"] * cheese_qty

        burger_data = {
            "bun": bun,
            "meat": meat,
            "sauce": sauce,
            "cheese_qty": cheese_qty,
            "id": BURGER_COUNT,
            "price": calculate_burger_price(ingredients),
            "timestamp": get_order_timestamp(),
        }

    except Exception as e:
        print(f"Error while assembling burger: {e}")
        return None

    burger = (
        f"{burger_data['bun']} bun + {burger_data['meat']} + "
        f"{burger_data['sauce']} + {burger_data['cheese_qty']}x cheese"
    )

    LAST_BURGER = burger
    print(f"\n🍔 Your burger: {burger}")
    print(f"💰 Total price (with tax): ${burger_data['price']:.2f}")
    print(f"🕒 Order timestamp: {burger_data['timestamp']}\n")

    return burger

def SaveBurger(burger):
    with open("/tmp/burger.txt", "w") as f:
        f.write(burger + "\n" + str(BURGER_COUNT))
    print("Burger saved to /tmp/burger.txt")

def MAIN():
    print("Welcome to the worst burger maker ever!\n")
    try:
        burger = AssembleBurger()
        if burger:
            SaveBurger(burger)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    MAIN()

