import json
import pandas as pd

with open('C:\\Git\\swiggy_restaurant_menu\\harshamess.json', 'r', encoding='utf-8') as f:
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

dishes = []

for card in data['data']['cards']:
    if 'groupedCard' in card:
        for group in card['groupedCard']['cardGroupMap']['REGULAR']['cards']:
            # Handle flat categories
            if 'card' in group and 'itemCards' in group['card']['card']:
                for item in group['card']['card']['itemCards']:
                    info = item['card']['info']
                    dishes.append({
                        'Restaurant': restaurant,
                        'City': city,
                        'Locality': locality,
                        'AreaName': areaName,
                        'DishName': info.get('name', ''),
                        'Price': info.get('price', 0) / 100
                    })
            # Handle nested categories (like in vashista.json)
            elif 'card' in group and 'categories' in group['card']['card']:
                for category in group['card']['card']['categories']:
                    groupName = category.get('title', '')
                    if 'itemCards' in category:
                        for item in category['itemCards']:
                            info = item['card']['info']
                            dishes.append({
                                'Restaurant': restaurant,
                                'City': city,
                                'Locality': locality,
                                'AreaName': areaName,
                                'GroupName': groupName,
                                'DishName': info.get('name', ''),
                                'Price': info.get('price', 0) / 100
                            })

df = pd.DataFrame(dishes)
df.to_excel('harshamess_menu.xlsx', index=False)

print("✅ Exported to vashista_menu.xlsx")