import postcodes_io_api
api  = postcodes_io_api.Api(debug_http=True)
data = api.get_postcode('SW112EF')
print(data)