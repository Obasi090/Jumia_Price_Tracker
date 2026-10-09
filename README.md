# Jumia Price Tracker

A Python application that retrieves product listings from Jumia Nigeria, allows users to select a product and set a target price, and sends an email notification when the product's current price is at or below the target price.

This project was built as part of the **100 Days of Code: The Complete Python Pro Bootcamp**.

## Features

* **Live product retrieval:** Fetches product listings using the ReefAPI Jumia API.
* **Category selection:** Allows users to choose a product category.
* **Product selection:** Displays available products and their current prices.
* **Target price tracking:** Compares a selected product's current price against the user's target price.
* **Email notifications:** Sends a price alert through Gmail SMTP when the target price is reached.
* **Input validation:** Handles invalid product selections and target-price inputs.
* **Error handling:** Handles common API request failures and email delivery errors.
* **Environment variables:** Keeps API credentials and email passwords outside the Python source code.

## Technologies Used

* Python
* Requests
* ReefAPI Jumia API
* python-dotenv
* Python `smtplib`
* Python `email.message`

## Project Structure

```text
Day_47_Jumia_Price_Tracker/
│
├── main.py
├── .env
├── .env.example
├── .gitignore
└── README.md
```

The `.env` file contains private credentials and should never be committed to GitHub.

## Requirements

Before running the project, make sure you have:

* Python installed.
* A ReefAPI account and a valid API key.
* A Gmail account configured for SMTP access.
* Git installed if you want to version-control the project.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd Day_47_Jumia_Price_Tracker
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

If you already have the project on your computer, you can skip this step.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install requests python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your credentials:

```text
JUMIA_API_KEY=your_reefapi_key
JUMIA_API_URL=https://api.reefapi.com/jumia/v1/category/products
MY_EMAIL=your_gmail_address
MY_PASSWORD=your_google_app_password
```

Replace the example values with your own credentials.

**Important:** For Gmail SMTP, use a Google App Password where supported rather than your regular Gmail password. Never share your `.env` file or publish your credentials.

### 5. Run the application

```bash
python main.py
```

Follow the prompts to select a product category, choose a product, enter your target price, and provide a recipient email address if the target price has been reached.

## How It Works

1. The application requests product listings from ReefAPI.
2. It displays the returned products and their current prices.
3. The user selects a product to track.
4. The user enters a target price.
5. The application compares the current price with the target price.
6. If the current price is less than or equal to the target price, the application sends an email alert.
7. Otherwise, it reports that the target price has not been reached.

## Limitations

* The application checks prices when it is run; it does not continuously monitor prices in the background.
* Product availability and prices depend on the API response and may change on Jumia.
* API usage may consume ReefAPI credits.
* Category identifiers must be supported by the API.
* Email delivery depends on valid Gmail SMTP credentials and network connectivity.
* The application does not currently persist tracking preferences or schedule future checks.

## Future Improvements

* Schedule recurring price checks.
* Store tracked products and target prices in a database.
* Notify users of price changes over time.
* Support multiple tracked products per user.
* Improve logging and automated testing.
* Add more robust email-address validation.

## Author

**Obasi Chukwunonso Glory**

A Python learning project focused on API integration, data handling, input validation, and email automation.
