from flask import Flask, jsonify, request, render_template
import requests
import pandas as pd

app = Flask(__name__)


def get_cocktails_by_ingredient(ingredient):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"
    response = requests.get(url)
    data = response.json()
    return data.get('drinks', [])


def get_cocktails_by_name(name):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    response = requests.get(url)
    data = response.json()
    drinks = data.get('drinks')
    if drinks is None:
        drinks = []
    return drinks


def get_cocktail_details(cocktail_id):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
    response = requests.get(url)
    data = response.json()
    return data.get('drinks', [])[0]


def get_random_cocktail():
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    data = response.json()
    return data.get('drinks')[0]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cocktails', methods=['GET'])
def cocktails():
    ingredient = request.args.get('ingredient', '')
    cocktails = get_cocktails_by_ingredient(ingredient)
    df = pd.DataFrame(cocktails)
    return jsonify(df.to_dict(orient='records'))


@app.route('/cocktails_by_name', methods=['GET'])
def cocktails_by_name():
    name = request.args.get('name', '')
    cocktails = get_cocktails_by_name(name)
    df = pd.DataFrame(cocktails)
    return jsonify(df.to_dict(orient='records'))


@app.route('/cocktail/<cocktail_id>', methods=['GET'])
def cocktail_detail(cocktail_id):
    details = get_cocktail_details(cocktail_id)
    return jsonify(details)


@app.route('/cocktail_random', methods=['GET'])
def cocktail_random():
    cocktail = get_random_cocktail()
    return jsonify(cocktail)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
