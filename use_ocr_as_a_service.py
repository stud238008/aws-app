import requests

response = requests.post(
    'YOUR URL',
    json={
        'bucket': "YOUR_BUCKET",
        'key': "YOUR_IMAGE_NAME"
    }
)

print(response.json())
