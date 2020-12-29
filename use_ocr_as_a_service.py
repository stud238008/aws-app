import base64

import requests

with open('test.jpg', 'rb') as file:
    base64_str = base64.b64encode(file.read()).decode()


response = requests.post(
    'https://1hene29fmj.execute-api.us-east-1.amazonaws.com/dev/ocr',
    json={
        'image': base64_str
    }
)

print(response.json())
