
import requests
import pandas as pd


restaurant_ID = 37968  # sample restaurant id. change the restaurant id to get menu of another restaurant.
# URL of the API endpoint
url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId=218478"
# Vashista's srilakshmi - 2498; Kakatiya mess - 3636; KR JH - 994612; KR HP - 994697; harsha - 218478; vashishtanizampet - 50099
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

# Send a GET request to the specified URL with headers
response = requests.get(url, headers=headers)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Extract JSON data from the response
    json_data = response.json()

    print(json_data)
    
    import json

    # Save the JSON data to a file
    with open("swiggy_response.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("✅ JSON data saved to swiggy_response.json")

    # Check if the restaurant data is present in the JSON response
    if 'cards' not in json_data['data'] or not json_data['data']['cards']:
        raise ValueError("No restaurant found with the given ID.")

    # Extract restaurant name from the json response
    restaurant_name = json_data['data']['cards'][0]['card']['card']

    # Initialize lists to store extracted data
    names = []
    categories = []
    descriptions = []
    prices_in_rupees = []

    # Extract relevant data and append to lists
    for card in json_data['data']['cards']:
        card_group_map = card.get('groupedCard', {}).get('cardGroupMap', {})
        regular_cards = card_group_map.get('REGULAR', {}).get('cards', [])
        for grouped_card in regular_cards:
            item_cards = grouped_card.get('card', {}).get('card', {}).get('itemCards', [])
            for item_card in item_cards:
                if item_card.get('card', {}).get('@type') == 'type.googleapis.com/swiggy.presentation.food.v2.Dish':
                    dish_info = item_card.get('card', {}).get('info', {})
                    names.append(dish_info.get('name', ''))
                    categories.append(dish_info.get('category', ''))
                    descriptions.append(dish_info.get('description', 'No description'))
                    price_in_paise = dish_info.get('price', 0)
                    price_in_rupees = price_in_paise / 100
                    prices_in_rupees.append(price_in_rupees)

    # Create a DataFrame
    df = pd.DataFrame({
        'Name': names,
        'Category': categories,
        'Description': descriptions,
        'Price': prices_in_rupees
    })

    # Save DataFrame to CSV file
    df.to_csv(f'{restaurant_name}_menu.csv', index=False)

    print("CSV file saved successfully.")
else:
    # Print an error message if the request was not successful
    print("Error accessing API. Status code:", response.status_code)
