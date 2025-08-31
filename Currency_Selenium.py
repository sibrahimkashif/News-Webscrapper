from selenium import webdriver
from selenium.webdriver.common.by import By

# setup driver
edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=edge_options)


def convert(c_from, c_to, amount, reference):
    url = f"https://www.x-rates.com/calculator/?from={c_from}&to={c_to}&amount={amount}"

    driver.get(url)

    converted_value = driver.find_element(By.CLASS_NAME, value="ccOutputRslt").text
    updated_date = driver.find_element(By.CLASS_NAME, value="calOutputTS").text

    if "0.000000" in converted_value:
        print("\n*An error occured*")
    else:
        if len(amount) == 0:
            amount = "1"
        print(f"\n{amount} {c_from} --> {converted_value}")

        if reference == True:
            pass


currencies = ["KWD", "EUR", "GBP", "USD", "CNY", "INR"]

while True:
    c_from = input("\nCurrency from (e.g USD) : ").upper().strip()
    if c_from == "Q":
        break
    c_to = input("Currency to (e.g PKR)   : ").upper().strip()
    amount = input("Amount (1) : ").strip()

    if c_from == "TOP":
        for currency in currencies:
            c_from = currency
            convert(c_from, c_to, amount, False)
        break
    elif c_to == "TOP":
        for currency in currencies:
            c_to = currency
            convert(c_from, c_to, amount, False)
        break

    else:
        convert(c_from, c_to, amount, True)

print()

driver.quit()
