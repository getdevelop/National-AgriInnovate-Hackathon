from flask import Flask, render_template, request
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

API_KEY = '579b464db66ec23bdd000001bde41887288942c463ea7a7c3fa3d66a'
API_URL = f'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={API_KEY}&format=csv&limit=100000'

def fetch_market_data():
    response = requests.get(API_URL)
    data = pd.read_csv(StringIO(response.text))
    return data

def filter_data(data, state=None, district=None, commodity=None, variety=None, grade=None, price_order=None):
    if state:
        data = data[data['State'] == state]
    if district:
        data = data[data['District'] == district]
    if commodity:
        data = data[data['Commodity'] == commodity]
    if variety:
        data = data[data['Variety'] == variety]
    if grade:
        data = data[data['Grade'] == grade]
    if price_order:
        data = data.sort_values(by='Min_x0020_Price', ascending=(price_order == 'low_to_high'))

    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/market-data', methods=['GET', 'POST'])
def market_data():
    data = fetch_market_data()
    filtered_data = data.copy()

    if request.method == 'POST':
        state = request.form.get('state')
        district = request.form.get('district')
        commodity = request.form.get('commodity')
        variety = request.form.get('variety')
        grade = request.form.get('grade')
        price_order = request.form.get('price_order')

        filtered_data = filter_data(data, state, district, commodity, variety, grade, price_order)


    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(filtered_data)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = filtered_data[start:end]

    data_dict = paginated_data.to_dict('records')

    states = data['State'].unique()
    districts = data['District'].unique()
    commodities = data['Commodity'].unique()
    varieties = data['Variety'].unique()
    grades = data['Grade'].unique()

    return render_template('market_data.html', data=data_dict, states=states,
                           districts=districts, commodities=commodities, varieties=varieties,
                           grades=grades, page=page, per_page=per_page, start=start, end=end, total=total)

if __name__ == '__main__':
    app.run(debug=True)
