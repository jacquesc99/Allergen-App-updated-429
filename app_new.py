import pandas as pd
from flask import Flask, render_template, request
app = Flask(__name__)
dishes = 'Allergens New.csv'
df = pd.read_csv(dishes)
df.columns = df.columns.str.strip().str.lower()
for col in df.columns[1:]:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "true": True,
            "false": False,
            "1": True,
            "0": False,
            "yes": True,
            "no": False
        })
        .fillna(False)
    )


@app.route('/', methods=['GET', 'POST'])
def index():

    allergens = df.columns.tolist()[1:]
    safe_results = []

    ALLERGENS= {"eggs", "dairy", "fish", "shellfish", "gluten", "peanuts", "tree nuts", "soy", "sesame", "capsacian", "piperine", "allium" }
    DIETARY = {"vegetarian", "vegan", "unpasturiezed cheese", "cured meats"}
    PREFERENCES = {"pork", "beef", "poultry"}

    if request.method == 'POST':
        #print("FORM DATA:", request.form)
        selected_allergens = [a.lower() for a in request.form.getlist('allergens')]
        print("selected_allergens:", selected_allergens)

        for _, row in df.iterrows():
            is_safe =True

            for allergen in selected_allergens:

                if allergen in df.columns:

                    if row[allergen]== True:
                        is_safe = False
                        break

            if is_safe:
                safe_results.append({
                    "dish": row.iloc[0],
            })


        return render_template('results.html', results= safe_results)

    return render_template('index.html', allergens= allergens)