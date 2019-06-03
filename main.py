import json
import postcodes_io_api
from flask import Flask, render_template, request
from haversine import haversine, Unit


def add_coordinates_alpha(list_of_places):
    """This function takes a list of dictionaries as an argument and appends
    additional dictionary pairs with data holding spacial coordinates.
    This version is slow due to the number of requests it is making.

    Parameters
    ----------
    list_of_places:list
        List of dictionaries with keys for name and postcode.

    Returns
    -------
    list_of_places:list
        List of dictionaries with added keys for longitude and latitude
    """

    for element in list_of_places:  # iteration over the list
        element['postcode'] = element['postcode'].replace(" ", "")  # removing spaces from postcodes
        is_valid = api.is_postcode_valid(element['postcode'])  # postcodes validity check
        if is_valid:  # creates new dictionary pair for storing coordinates if valid
            element['lon'] = api.get_postcode(element['postcode'])['result']['longitude']
            element['lat'] = api.get_postcode(element['postcode'])['result']['latitude']
        else:
            element['lon'] = 'error'
    return list_of_places


def add_coordinated_beta(list_of_places):
    """This function takes a list of dictionaries as an argument and appends
    additional dictionary pairs with data holding spacial coordinates.
    This method is faster because it makes only one bulk request.

    Parameters
    ----------
    list_of_places:list
        List of dictionaries with keys for name and postcode.

    Returns
    -------
    list_of_places:list
        List of dictionaries with added keys for longitude and latitude
    """

    unpacked_list_dict_places_result = unpacking_api_data(list_of_places)
    a = 0
    for element in list_of_places:
        if unpacked_list_dict_places_result[a] is not None:  # postcode validity check
            element['lat'] = unpacked_list_dict_places_result[a]['latitude']
            element['lon'] = unpacked_list_dict_places_result[a]['longitude']
            a = a + 1
        else:
            element['lon'] = 'error'
            a = a + 1
    return list_of_places


def unpacking_api_data(list_of_data_dictionaries):
    """This function using json data as a template, creates list of postcodes and using api translates them
     to cluttered sets of data. Data is cleaned by series of operations and the result is list
     of dictonaries with names, postcodes and coordinates.

     Parameters
     ----------

     list_of_data_dictionaries:list
        Template which is translated to postcodes with stores.
    """

    unpacked_list_dict_places = []
    postcodes_string_list = [i['postcode'] for i in list_of_data_dictionaries]
    bulk_postcodes = api.get_bulk_postcodes(postcodes_string_list)
    bulk_postcodes_unpacked = [i for i in bulk_postcodes['result']]
    for temp in bulk_postcodes_unpacked:
        unpacked_list_dict_places.append(temp['result'])
    return unpacked_list_dict_places


def make_nearest_towns_list(my_postcode, desired_max_distance):
    """It reads postcode of the user, translate it to coordinates, remove errors and using haversine function it
    returns list of towns which are nearer then max distance submitted from the form.

    Parameters
    ----------
    my_postcode:str
        Postcode translated later by api to coordinates.
    desired_max_distance:float
        Radius within which user wants to find stores.

    Returns
    -------
    list_of_dictionaries_of_nearest_towns:list
        Dictionaries have got keys for name, postcode and latitude.
    """
    list_of_dictionaries_of_nearest_towns.clear()  # Clearing allows to easily submit next queries after the first one
    postcode_info = api.get_postcode(my_postcode.upper())
    my_location_latitude = postcode_info['result']['latitude']
    my_location_longitude = postcode_info['result']['longitude']
    res = [i for i in sorted_json_list if i['lon'] != 'error']
    for element in res:
        actual_distance = haversine((my_location_latitude, my_location_longitude), (element['lat'], element['lon']),
                                    unit=Unit.MILES)
        if int(actual_distance) < int(desired_max_distance):
            list_of_dictionaries_of_nearest_towns.append(
                {'name': element['name'], 'postcode': element['postcode'], 'latitude': element['lat']})
    return list_of_dictionaries_of_nearest_towns


def preparing_stores_data(filename):
    """Build sorted by name list of dictionaries with data for postcodes from filename.
    This sorted places will be displayed on the home website.

    Parameters
    ----------
    filename:str
        The name of the file.The file has to be in the same folder as main.py.

    Returns
    -------
    list
        List of sorted by name dictionaries with keys for name and postcode.
    """

    with open(filename, "r") as stores:
        data = stores.read()
    obj = json.loads(data)
    return sorted(obj, key=lambda i: i['name'])  # sorting by name key


app = Flask(__name__)  # Creating Flask object
api = postcodes_io_api.Api(debug_http=False)
list_of_dictionaries_of_nearest_towns = []
sorted_json_list = preparing_stores_data("stores.json")  # creates list of dictionaries with name and postcode from json
# sortedList = add_coordinates_alpha(sortedList)
sorted_json_list = add_coordinated_beta(sorted_json_list)  # adding coordinates


@app.route("/")
def result():
    """Renders home page with sorted table of towns with stores.
    """

    return render_template("home.html", result=sorted_json_list)


@app.route('/storeslist', methods=['POST'])
def storeslist():
    if request.method == 'POST':
        my_query = request.form
        if api.is_postcode_valid(my_query['postcode']) and int(my_query['distance']) > 0:  # validation check
            nearest_towns = make_nearest_towns_list(my_query['postcode'], int(my_query['distance']))
            sorted_by_lat_nearest_towns = sorted(nearest_towns, key=lambda i: i['latitude'], reverse=True)
            return render_template("storeslist.html", nearest_stores=sorted_by_lat_nearest_towns,
                                   how_many=len(sorted_by_lat_nearest_towns))


if __name__ == "__main__":  # running the application
    app.run(debug=True, threaded=True)
