import json
import postcodes_io_api
from flask import Flask, render_template, request

with open("stores.json", "r") as stores:
    data = stores.read()

obj = json.loads(data)
api = postcodes_io_api.Api(debug_http=True)
app = Flask(__name__)


@app.route("/")
def result():
    sortedList = sorted(obj, key=lambda i: i['name'])
    for ell in sortedList:
        ell['postcode'] = ell['postcode'].replace(" ", "")
        is_valid = api.is_postcode_valid(ell['postcode'])
        if is_valid:
            ps = api.get_postcode(ell['postcode'])
            ell['lon'] = api.get_postcode(ell['postcode'])['result']['longitude']
            ell['lat'] = api.get_postcode(ell['postcode'])['result']['latitude']
        else:
            ell['lon'] = 'error'
    return render_template("home.html", result=sortedList)


@app.route('/storeslist', methods=['POST'])
def storeslist():
    if request.method == 'POST':
        storeslist = request.form
        data = api.get_nearest_postcodes_for_postcode(postcode=storeslist['postcode'], radius=storeslist['distance'])
        return render_template("storeslist.html", storeslist=data)


if __name__ == "__main__":
    app.run(debug=True)
