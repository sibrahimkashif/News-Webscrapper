from bs4 import BeautifulSoup
import requests, json, datetime

country_mappings = {
    "Pk": "Pakistan",
    "Sa": "Saudi-Arabia",
}

city_mappings = {
    "Madina": "Medina",
    "Makkah": "Mecca",
}

while True:
    j = 0
    weather_type = input("\nWhat weather do you want to view (Current 1/Forecast 2): ").strip().lower()

    if weather_type == "current" or weather_type == 1:
        city = input("\nEnter a City: ").strip().title()

        # fix misspelled city names
        city = city_mappings.get(city, city)

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=3af6a928cddb412aeb910ed4c8ad4d57&units=metric"

        response = requests.get(url)

        # if successful
        if response.status_code == 200:
            data = response.json()
            country = data["sys"]["country"]
            weather = data["weather"][0]["description"]
            temperature = int(data["main"]["temp"])
            feels_like = int(data["main"]["feels_like"])
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            datetime_object = str(datetime.datetime.fromtimestamp(data["dt"]))

            print(
                f"Weather for {city} on {datetime_object[:10]}:\n"
                f"\n"
                f"Weather:      {weather.title()}\n"
                f"Temperature:  {temperature}°C\n"
                f"Feels like:   {feels_like}°C\n"
                f"Humidity:     {humidity}%\n"
                # f"Wind speed:   {wind_speed} KM/H\n"
                f"\nLast updated: {datetime_object}\n"
            )

        else:
            print("*Error: Invalid city name*\n")

    elif weather_type == "forecast" or weather_type == 2:
        forecast_type = input("\n24-hour forecast (1) or 14-day forecast (2)? ")

        country = input("\nEnter a Country: ").title()

        if country == "Default":
            country = "Pk"
            city = "Karachi"

        city = input("Enter a City: ").title()

        country = country_mappings.get(country, country)
        city = city_mappings.get(city, city)

        if forecast_type == "1":
            url = f"https://www.timeanddate.com/weather/{country}/{city}/hourly"
        else:
            url = f"https://www.timeanddate.com/weather/{country}/{city}/ext"

        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")

        # Extract relevant data from the HTML page
        error_tags = soup.find_all(class_="headline-banner__title")
        script_tags = soup.find_all("script")
        update_tags = soup.find_all("tfoot")

        for error in error_tags:
            print(f"\n*{error.text}*")

        # Loop through each <script> tag to get weather details
        for script in script_tags:
            script_content = script.string

            # Check if the script content exists and contains 'var data'
            if script_content and "var data" in script_content:
                # Extract the value of 'var data' from the script content
                start_index = script_content.find("var data") + len("var data=")
                end_index = script_content.find(";", start_index)
                var_data = script_content[start_index:end_index].strip()

                data = json.loads(var_data)

                # Loop through each day's weather details
                for day in data["detail"]:
                    date = day["ds"]
                    desc = day["desc"]
                    temp_max = day["temp"]
                    if forecast_type == "2":
                        temp_min = day["templow"]
                    feels_like = day["cf"]
                    wind = day["wind"]
                    humidity = day["hum"]
                    rain = day["pc"]

                    # Display a special alert for high rain chances
                    alert = "***" if int(rain) > 50 else ""

                    temp_min = f"/{temp_min}" if forecast_type == "2" else ""

                    j += 1

                    if j == 25:
                        break

                    print(
                        f"{j}) {date}:\n"
                        f"    Weather:      {desc}\n"
                        f"    Temperature:  {temp_max}{temp_min}°C\n"
                        f"    Feels_like:   {feels_like}°C\n"
                        f"    Wind:         {wind} KM/H\n"
                        f"    Humidity:     {humidity}%\n"
                        f"    Rain chances: {alert}{rain}%{alert}\n"
                    )

        # Print last updated tag if available
        if "Day" in str(error_tags):
            for item in update_tags:
                print(item.text, "\n")

    else:
        print("\n*Error: Please choose from the given options*")
        continue
