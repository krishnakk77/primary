import pandas as pd
from difflib import get_close_matches

# Load both sheets
file = 'kammanivsharshamess_menu.xlsx'
harshamess = pd.read_excel(file, sheet_name='Sheet1')
kammani = pd.read_excel(file, sheet_name='Sheet2')

# Normalize dish names for matching
harshamess['DishNameNorm'] = harshamess['DishName'].str.lower().str.replace(r'[^a-z0-9 ]', '', regex=True).str.strip()
kammani['DishNameNorm'] = kammani['DishName'].str.lower().str.replace(r'[^a-z0-9 ]', '', regex=True).str.strip()

# Prepare comparison list
comparison = []

for idx, v_row in harshamess.iterrows():
    # Find closest match in Kammani
    matches = get_close_matches(v_row['DishNameNorm'], kammani['DishNameNorm'], n=1, cutoff=0.85)
    if matches:
        k_row = kammani[kammani['DishNameNorm'] == matches[0]].iloc[0]
        harshamess_price = v_row['Price']
        kammani_price = k_row['Price']
        if harshamess_price > kammani_price:
            more_expensive = "harshamess"
        elif harshamess_price < kammani_price:
            more_expensive = "Kammani Ruchulu"
        else:
            more_expensive = "Same Price"
        comparison.append({
            'Dish Name': v_row['DishName'],
            "harshamess's Price": harshamess_price,
            "Kammani Price": kammani_price,
            "Which Restaurant is More Expensive": more_expensive
        })

# Export to Excel
df_report = pd.DataFrame(comparison)
df_report.to_excel('price_comparison_report1.xlsx', index=False)
print("✅ Price comparison report exported to price_comparison_report1.xlsx")