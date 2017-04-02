from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
app.debug = True

def data():
    today = datetime.now().strftime("%d-%m-%Y")
    days_ago = (datetime.now() + timedelta(days=-30)).strftime("%d-%m-%Y")
    daterange = '&daterange=' + days_ago + '-' + today
    contracts_api = "http://openapi.clearspending.ru/restapi/v3/contracts/search/?pricerange=5000000000-1000000000000" + daterange
    r = requests.get(contracts_api)
    return r.json()['contracts']['data']


@app.route('/')
def list_contracts():
    list_of_big_contracts = data()
    return render_template("contracts.html",
                           data=list_of_big_contracts)

@app.route('/contract/<int:n>')
def contract_details(n):
    details = data()[n-1]
    if details['fz'] == '223':
        url = 'http://zakupki.gov.ru/223/contract/public/contract/view/general-information.html?id=' \
              + details['printFormUrl'][86:93] + '&viewMode=FULL'
    else:
        url = details['contractUrl']


    return render_template("contract_details.html", contract=details, contract_url = url)



if __name__ == '__main__':
    app.run()