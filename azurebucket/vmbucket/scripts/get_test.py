# importing the requests library 
import requests 
  
host ="VM3"

# defining the api-endpoint  
API_ENDPOINT = "http://localhost:8000/vmbucket/"
API_URL = API_ENDPOINT + host + "/"

print(API_ENDPOINT)
  
# your API key here 
#API_KEY = "XXXXXXXXXXXXXXXXX"
  
# your source code here 
source_code = ''' 
print("Hello, world!") 
a = 1 
b = 2 
print(a + b) 
'''
  
# data to be sent to api 
data = {'name':"VM3", 
        'subscription':'sub3'
        } 
  
# sending post request and saving response as response object 
#r = requests.post(url = API_ENDPOINT, data = data) 
r = requests.get(url = API_ENDPOINT) 
  
# extracting response text  
pastebin_url = r.text 
#print("The pastebin URL is:%s"% r.headers['Content-Length']) 

if r.headers['Content-Length'] == "2":
    print("The record does not exist")
else:
    print('The record exists')