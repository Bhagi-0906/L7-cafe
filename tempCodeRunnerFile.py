import mysql.connector
from tabulate import tabulate

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",       # Replace with your MySQL username
    password="abcJK9!",   # Replace with your MySQL password
    database="IceCreamParlor"
)
cursor = db.cursor()

# Function to display seasonal offerings
def view_seasonal_offerings():
    cursor.execute("SELECT id, flavor_name, description, price FROM SeasonalOfferings")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=["ID", "Flavor", "Description", "Price"], tablefmt="pretty"))

# Function to search and filter offerings
def search_offerings(keyword):
    query = "SELECT id, flavor_name, description, price FROM SeasonalOfferings WHERE flavor_name LIKE %s"
    cursor.execute(query, (f"%{keyword}%",))
    rows = cursor.fetchall()
    print(tabulate(rows, headers=["ID", "Flavor", "Description", "Price"], tablefmt="pretty"))

# Function to add allergens
def add_allergen(allergen_name):
    try:
        cursor.execute("INSERT INTO Allergens (allergen_name) VALUES (%s)", (allergen_name,))
        db.commit()
        print("Allergen added successfully!")
    except mysql.connector.IntegrityError:
        print("Allergen already exists.")

# Function to add items to the cart
def add_to_cart(flavor_id, quantity):
    cursor.execute("INSERT INTO Cart (flavor_id, quantity) VALUES (%s, %s)", (flavor_id, quantity))
    db.commit()
    print("Item added to cart!")

# Function to view cart
def view_cart():
    query = """
    SELECT Cart.id, SeasonalOfferings.flavor_name, Cart.quantity, 
           (SeasonalOfferings.price * Cart.quantity) AS total_price
    FROM Cart
    JOIN SeasonalOfferings ON Cart.flavor_id = SeasonalOfferings.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print(tabulate(rows, headers=["Cart ID", "Flavor", "Quantity", "Total Price"], tablefmt="pretty"))

# Main menu
def main_menu():
    while True:
        print("\n--- Ice Cream Parlor Menu ---")
        print("1. View Seasonal Offerings")
        print("2. Search Offerings")
        print("3. Add Allergen")
        print("4. Add to Cart")
        print("5. View Cart")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            view_seasonal_offerings()
        elif choice == "2":
            keyword = input("Enter keyword to search: ")
            search_offerings(keyword)
        elif choice == "3":
            allergen = input("Enter allergen name: ")
            add_allergen(allergen)
        elif choice == "4":
            flavor_id = int(input("Enter Flavor ID: "))
            quantity = int(input("Enter quantity: "))
            add_to_cart(flavor_id, quantity)
        elif choice == "5":
            view_cart()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the application
if __name__ == "__main__":
    main_menu()
