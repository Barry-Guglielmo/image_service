import requests
from config import *

# Test Pushing A Static Image
data = {"first": "scinamic", "second": 'curves'}
image_path = 'templates/rick.jpeg'
file = {'file': ('rick.jpeg', open(image_path, 'rb'))}
response = requests.post(API_UPLOAD_URL, files=file, data=data )
print(response)

# Test Getting the Image
endpoint = '%s/%s/%s/%s'%('http://127.0.0.1:5000//livedesign/images',data['first'],data['second'],'rick.jpeg')
print(endpoint)
response = requests.get(endpoint)
print(response)