import base64
import io
import json
import os
import boto3

from PIL import Image
import pytesseract

if os.getenv('AWS_EXECUTION_ENV') is not None:
    os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
    os.environ['TESSDATA_PREFIX'] = '/opt/tessdata'
    pytesseract.pytesseract.tesseract_cmd = '/opt/tesseract'


def ocr(event, context):
    request_body = json.loads(event['body'])
    
    bucket = request_body['bucket']
    key = request_body['key']
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    body = obj.get()['Body']
    
    text = pytesseract.image_to_string(Image.open(body))

    body = {
        "text": text
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
