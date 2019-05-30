import json
from flask import Flask,render_template
import postcodes_io_api
api  = postcodes_io_api.Api(debug_http=True)
ps = api.get_postcode('SW112EF')


print(ps)


with open("stores.json","r") as stores:
    data = stores.read()

obj=json.loads(data)

print(data)
print(type(data))
print(obj)
print(type(obj))
print(type(obj[0]))

#sr=sorted(obj,key=lambda i:i['name'])
#print(sr)

app=Flask(__name__)

@app.route("/")
def result():
    sortedList = sorted(obj, key=lambda i: i['name'])
    print(sortedList)
    #dict={'phy':50,'che':60,"math":34}
    return render_template("home.html",result=sortedList)

if __name__ == "__main__":
    app.run(debug=True)