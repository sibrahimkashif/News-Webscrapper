from bs4 import BeautifulSoup
import requests


def convert(amount, c_to, c_from, reference):
    url = f"https://www.x-rates.com/calculator/?from={c_from}&to={c_to}&amount={amount}"

    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")

    converted = soup.find(class_="ccOutputRslt")
    updated = soup.find(class_="calOutputTS")

    if "0.000000" in converted.text:
        print("\n*An error occured*")
    else:
        if len(amount) == 0:
            amount = "1"
        print(f"\n{amount} {c_from} -> {round(converted.text.float(),3)}")

        if reference == True:
            pass
            # print(f"\n(Last updated: {updated.text})")


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
            convert(amount, c_to, c_from, False)
        break
    elif c_to == "TOP":
        for currency in currencies:
            c_to = currency
            convert(amount, c_to, c_from, False)
        break

    else:
        convert(amount, c_to, c_from, True)

print()
