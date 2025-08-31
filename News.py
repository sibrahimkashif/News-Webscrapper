from bs4 import BeautifulSoup
import requests

# fix skyports football, f1, and nba

while True:
    website = (
        input("\nSelect a News website [The News (1)/Sky Sports (2)]: ").strip().title()
    )

    if website:
        website_mappings = {
            "1": "The News",
            "2": "SkySports",
        }
        website = website_mappings.get(website, website)

    if website == "The News":
        print(
            "\nCategories: Latest (1), National (2), Sports (3), World (4), Business (5), Entertainment (6), Tech (7), Health (8)"
        )
        category = input("\nSelect a category: ").title().strip()

        if category:
            category_mappings = {
                "1": "Latest",
                "2": "National",
                "3": "Sports",
                "4": "World",
                "5": "Business",
                "6": "Entertainment",
                "7": "Tech",
                "8": "Health",
            }

        category = category_mappings.get(category, category)

        if category not in str(category_mappings) or len(category) < 2:
            print("\n<Error: Please choose from the given categories>\n")
            continue

        # handle website url exceptions
        if category == "Latest":
            url = "https://www.thenews.com.pk/latest-stories"
        elif category == "Tech":
            url = f"https://www.thenews.com.pk/latest/category/Sci-tech"
        else:
            url = f"https://www.thenews.com.pk/latest/category/{category}"

        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")

        if category in ["Technology", "Tech", "Entertainment", "Business", "Health"]:
            headlines = soup.find_all(class_="open-section")
            i=0
            for headline in headlines:
                i+=1
                if "h2" in str(headline) and i%2==0:
                    print(">")
                    print(headline.text)
        else:
            headlines = soup.find_all(class_="writter-list-item-story")
            for headline in headlines:
                print(">")
                print("\n\n", headline.text.strip(), "\n\n")

        print(">\n")

        print(f"Source: {url}\n")

    elif website == "SkySports":
        print("\nCategories: Football (1), Cricket (2), Tennis (3), F1 (4), NBA (5)")

        category = input("Select a category: ").lower().strip()

        if category:
            category_mappings = {
                "1": "Football",
                "2": "Cricket",
                "3": "Tennis",
                "4": "F1",
                "5": "NBA",
            }
        try:
            category = category_mappings.get(category, category)
        except NameError:
            continue

        if category not in str(category_mappings) or len(category) < 2:
            print("\n<Please choose from the given categories>\n")
            continue

        url = f"https://www.skysports.com/{category.lower()}/news"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")

        if category in ["NBA", "Tennis", "Cricket"]:
            headings = soup.find_all(class_="sdc-site-tile__headline-text")
        else:
            headings = soup.find_all(
                class_="news-list__item news-list__item--show-thumb-bp30"
            )

        # print the contents of the tags
        for heading in headings:
            print(">")
            print(heading.text.strip(), "\n")

        print(">\n")

        print(f"Source: {url}\n")
    else:
        print("<An error occured, please choose from the shown websites>")
