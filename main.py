import json
from flask import Flask,render_template,request
import postcodes_io_api


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
api = postcodes_io_api.Api(debug_http=True)
app=Flask(__name__)

@app.route("/")
def result():
    sortedList = sorted(obj, key=lambda i: i['name'])
    #api = postcodes_io_api.Api(debug_http=True)
    for ell in sortedList:
        #ell['lon']=3
        #api = postcodes_io_api.Api(debug_http=True)
        ell['postcode']=ell['postcode'].replace(" ","")
        is_valid=api.is_postcode_valid(ell['postcode'])
        if (is_valid==True):
            ps = api.get_postcode(ell['postcode'])
            print("\ntype of ps:{}".format(type(ps)))
            langit=ps['result']['longitude']
            latid=ps['result']['latitude']
            print(langit)
            ell['lon'] = api.get_postcode(ell['postcode'])['result']['longitude']
            ell['lat'] = api.get_postcode(ell['postcode'])['result']['latitude']
        else:
            ell['lon'] = 'error'
    #     #lan=api.get_postcode(ell['postcode'])['result']['longitude']
    #     ell['lan']=api.get_postcode(ell['postcode'])['result']['longitude']
    print("\nSSSSSSSSOOOOORRRTTEED \nLLLLIIIISSSTTT")
    print("sortedList: {}".format(sortedList))
    #dict={'phy':50,'che':60,"math":34}
    return render_template("home.html",result=sortedList)

@app.route('/storeslist',methods=['POST'])
def storeslist():
    if(request.method=='POST'):
        storeslist=request.form
        print("storeslist:{}".format(storeslist))
        data = api.get_nearest_postcodes_for_postcode(postcode=storeslist['postcode'], radius=storeslist['distance'])
        print("data:{}".format(data))
        return render_template("storeslist.html",storeslist=data)

if __name__ == "__main__":
    app.run(debug=True)