import json
import postcodes_io_api
from flask import Flask, render_template, request
from haversine import haversine, Unit


def add_coordinates(list_of_places):
    """This function takes a list of dictionaries as an argument and appends
    additional dictionary pairs with data holding spacial coordinates"""
    for element in list_of_places:  # iteration over the list
        element['postcode'] = element['postcode'].replace(" ", "")  # removing spaces from postcodes
        is_valid = api.is_postcode_valid(element['postcode'])  # postcodes validity check
        if is_valid:  # creates new dictionary pair for storing coordinates if valid
            element['lon'] = api.get_postcode(element['postcode'])['result']['longitude']
            element['lat'] = api.get_postcode(element['postcode'])['result']['latitude']
        else:
            element['lon'] = 'error'
    return list_of_places


def make_nearest_towns_list(my_postcode, chosen_distance):
    postcode_info=api.get_postcode(my_postcode)
    my_location_latitude=postcode_info['result']['latitude']
    my_location_longitude=postcode_info['result']['longitude']
    # print(my_location_latitude,my_location_longitude)
    # print("postcode info:",postcode_info)
    add_coordinates(sortedList)
    # print(sortedList)
    for ellll in sortedList[4:]:
        print(ellll['name'])
        jakdaleko=haversine((my_location_latitude,my_location_longitude),(ellll['lat'],ellll['lon']),unit=Unit.MILES)
        if int(jakdaleko)<int(chosen_distance):
            list_of_nearest_towns.append(ellll['name'])
    print("\nList of nearest towns",list_of_nearest_towns)
    print("There is {} towns in range".format(len(list_of_nearest_towns)))
    return list_of_nearest_towns


with open("stores.json", "r") as stores:
    data = stores.read()
obj = json.loads(data)
api = postcodes_io_api.Api(debug_http=False)
app = Flask(__name__)  # Creating Flask object
sortedList = sorted(obj, key=lambda i: i['name'])  # sorting by name key
list_of_nearest_towns=[]
sortedList = add_coordinates(sortedList)

@app.route("/")
def result():
    return render_template("home.html", result=sortedList)


@app.route('/storeslist', methods=['POST'])
def storeslist():
    if request.method == 'POST':
        my_query = request.form
        # print("\nstorelist:\n"+str(storeslist))
        # print("type of storelist: ",type(storeslist))
        if api.is_postcode_valid(my_query['postcode']) and int(my_query['distance']) > 0:  # validation check
            # near = api.get_nearest_postcodes_for_postcode(postcode=storeslist['postcode'], radius=storeslist['distance'])
            # print(near)
            # print("type of near{}".format(type(near)))
            make_nearest_towns_list(my_query['postcode'],int(my_query['distance']))
            # sorted_near=sorted(near['result'], key=lambda i: i['latitude'])
            # print(sorted_near)
            # print("a wiec lista najblizszych miast",list_of_nearest_towns)
            return render_template("storeslist.html", nearest_stores=list_of_nearest_towns)


if __name__ == "__main__":  # running the application
    app.run(debug=True, threaded=True)
