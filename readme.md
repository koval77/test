# Test website

## Website made withPython and Flask of the online shop. The program takes as an input localisation (with postcode) from the user and a some distance and then it generates an list of the nearby shops. 

It uses the haversine formula which determines the great-circle distance between two points on a sphere given their longitudes and latitudes.

### How to use it:

1. Make sure that you have python installed
2. Make sure path to python is specified in your environmental variables [environment variables tutorial](https://geek-university.com/python/add-python-to-the-windows-path/)
3. Before running the applicataion all the dependincies has to be installed first. Run this command in cmd or powershell:
`pip install -r requirements.txt` from inside the folder "test".
4. From folder "test" run command: 
`python main.py`
5. Server will run on local host. Open the browser and put http://127.0.0.1:5000/ into address bar (assuming default settings)
6. Website will be opened. Into the form fields insert user postcode and desired distance.

## Working demo

[Try it out](https://limitless-mesa-45752.herokuapp.com/)

# Troubleshooting

If there will be problem with installation dependencies from requirements.txt try following commands installing the most basic libraries:
`pip install --user postcodes-io-api`
`pip install --user flask`
`pip install --user haversine`
