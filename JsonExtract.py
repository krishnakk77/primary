import json
import pandas as pd
# Replace with your file path
with open('C:\\Git\\swiggy_restaurant_menu\\vashista.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find restaurant info
restaurant_info = None
for card in data['data']['cards']:
    if 'card' in card and 'info' in card['card']['card']:
        restaurant_info = card['card']['card']['info']
        break

restaurant = restaurant_info.get('name', '')
city = restaurant_info.get('city', '')
locality = restaurant_info.get('locality', '')
areaName = restaurant_info.get('areaName', '')

# Extract dishes
dishes = []
for card in data['data']['cards']:
    if 'groupedCard' in card:
        for group in card['groupedCard']['cardGroupMap']['REGULAR']['cards']:
            if 'card' in group and 'itemCards' in group['card']['card']:
                for item in group['card']['card']['itemCards']:
                    info = item['card']['info']
                    dishes.append({
                        'Restaurant': restaurant,
                        'City': city,
                        'Locality': locality,
                        'AreaName': areaName,
                        'DishName': info.get('name', ''),
                        'Price': info.get('price', 0) / 100  # Swiggy prices are in paise
                    })

# Print the first 10 dishes
for row in dishes[:10]:
    print(row)


# Create a DataFrame and export to Excel
df = pd.DataFrame(dishes)
df.to_excel('vashista_menu.xlsx', index=False)

print("✅ Exported to kammani_menu.xlsx")

