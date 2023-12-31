import requests
from config import *

# Test Pushing A Static Image
data = {"first": "scinamic", "second": 'curves'}
image_path = 'templates/rick.jpeg'
file = {'file': ('rick.jpeg', open(image_path, 'rb'))}
response = requests.post(API_UPLOAD_URL, files=file, data=data )
print(response.text)

# Test Getting the Image
endpoint = '%s/%s/%s/%s'%(BASE_URL+'/livedesign/images',data['first'],data['second'],'rick.jpeg')
print(endpoint)
response = requests.get(endpoint)
print(response)
