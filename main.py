import requests
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

def jumia_api_request(category):
    JUMIA_API_KEY = os.getenv("JUMIA_API_KEY")
    JUMIA_API_URL = os.getenv("JUMIA_API_URL")

    if not JUMIA_API_KEY or not JUMIA_API_URL:
        raise RuntimeError("Missing JUMIA_API_KEY or JUMIA_API_URL — check your .env file.")

    payload = {
        "category": category, #The user needs to input the category by themselves
        "country": "ng"
    }

    headers = {
        "x-api-key": JUMIA_API_KEY,
        "content-type": "application/json"
    }

    try:
        response = requests.post(JUMIA_API_URL,
                                 headers=headers,
                                 json=payload,
                                 timeout=30
                                 )
        response.raise_for_status()

        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(
                f"ReefAPI returned an error: {data.get('error')}"
            )
        return data["data"]["results"]

    except requests.HTTPError as error:
        print(f"API returned an HTTP error: {error}")
    except requests.Timeout:
        print("The request timed out.")
    except requests.ConnectionError as error:
        print(f"Could not connect to ReefAPI: {error}")
    except requests.exceptions.JSONDecodeError:
        print("The API response was not valid JSON.")
    except requests.RequestException as error:
        print(f"An error occurred while making the API request: {error}")

    return None

def get_category():
    categories = {
        "1": "phones-tablets",
        "2": "computing",
        "3": "electronics",
        "4": "home-office",
        "5": "fashion",
        "6": "groceries"
    }

    print("\nAvailable Jumia categories:")
    for number, category in categories.items():
        print(f"{number}. {category.replace('-', ' ').title()}")

    while True:
        choice = input("Choose a category number: ").strip()

        if choice in categories:
            return categories[choice]

        print("Invalid choice. Please select one of the listed numbers.")

def display_products(products):
    for number, product in enumerate(products, start=1):
        print(
            f"{number}. {product.get('title', 'Untitled product')}\n"
            f"   Price: {product.get('currency', 'NGN')} "
            f"{product.get('price')}\n"
        )


def select_product(products):
    while True:
        try:
            choice = int(
                input("Enter the number of the product you want to track: ")
            )

            if choice < 1 or choice > len(products):
                print(
                    f"❌ Error: Please choose a number between 1 and {len(products)}."
                )
                continue

            break

        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")

    return products[choice - 1]


def get_target_price():
    while True:
        try:
            target_price = int(input("Enter your target price: N"))

            if target_price < 0:
                print("The target price cannot be negative.")
                continue

            return target_price

        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")


def check_price(product, target_price):
    product_name = product.get("name") or product.get("title")
    current_price = product.get("price")
    product_url = product.get("url")

    if current_price is None:
        print("The selected product has no available price.")
        return None

    try:
        current_price = float(current_price)
    except (ValueError, TypeError):
        print("The product price could not be read.")
        return None

    if current_price <= target_price:
        print(
            f"This product is available for N{current_price}!\n"
        )
        return product_name, current_price, target_price, product_url

    print(
        f"This is currently N{current_price}.\n"
        f"The current price is above your target price of N{target_price}."
    )
    return False

def send_email(product_name, current_price, target_price, product_url):
    my_email = os.getenv("MY_EMAIL")
    my_password = os.getenv("MY_PASSWORD")

    if not my_email or not my_password:
        print("Missing MY_EMAIL or MY_PASSWORD in your .env file.")
        return

    user_email = input("Enter your email: ").strip().lower()

    if not user_email:
        print("No recipient email address was provided.")
        return

    msg = EmailMessage()
    msg["Subject"] = "Jumia Price Alert — Your Target Price Has Been Reached!"
    msg["From"] = my_email
    msg["To"] = user_email

    msg.set_content(
        f"Hello,\n\n"
        f"Good news! The product you are tracking on Jumia "
        f"has reached your target price.\n\n"
        f"Product: {product_name}\n"
        f"Current Price: N{current_price:,.2f}\n"
        f"Your Target Price: N{target_price:,.2f}\n\n"
        f"View the product here:\n{product_url}\n\n"
        f"Happy shopping!\n\n"
        f"Jumia Price Tracker"
    )
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(my_email, os.getenv("MY_PASSWORD"))
            smtp.send_message(msg)
        print("Email sent successfully!")
    except (smtplib.SMTPException, OSError) as error:
        print(f"Could not send the email: {error}")

def main():
    category = get_category()
    print(f"\nFetching products in {category.replace('-', ' ')}...")

    products = jumia_api_request(category)
    if products is None:
        print("Unable to retrieve products. Please try again later.")
        return

    if not products:
        print("No products were returned for this category.")
        return

    display_products(products)

    selected_product = select_product(products)

    print(
        f"\nSelected product: "
        f"{selected_product.get('name') or selected_product.get('title')}\n"
        f"Current price: N{selected_product.get('price')}"
    )

    target_price = get_target_price()

    price_reached = check_price(selected_product, target_price)

    if price_reached:
        product_name, current_price, target_price, product_url = price_reached
        if product_url:
            send_email(product_name,
                       current_price,
                       target_price,
                       product_url)
        else:
            print("The product URL is missing, so the email was not sent.")

if __name__ == "__main__":
    main()