import base64
import io
import json
import os
import boto3

from PIL import Image
from pytesseract import image_to_data, Output, pytesseract

if os.getenv('AWS_EXECUTION_ENV') is not None:
    os.environ['LD_LIBRARY_PATH'] = '/opt/lib'
    os.environ['TESSDATA_PREFIX'] = '/opt/tessdata'
    pytesseract.tesseract_cmd = '/opt/tesseract'


def ocr(event, context):
    request_body = json.loads(event['body'])
    
    bucket = request_body['bucket']
    key = request_body['key']
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    body = obj.get()['Body']
    
    data = image_to_data(Image.open(body), output_type=Output.DICT)

    response = {
        "statusCode": 200,
        "body": prepare_results(data)
    }

    return response

def prepare_results(data):
    confidences = data['conf']
    text_blocks = data['text']
    words_nums = data['word_num']

    first_char_index = None

    text_block_entries = []
    confidence_entries = []

    for index, vals in enumerate(zip(confidences, text_blocks, words_nums)):
        conf, text, word_num = vals

        if first_char_index is None and word_num > 0:
            first_char_index = index

        if first_char_index:
            if word_num == 0:
                text_block_entries.append('\n')
            else:
                if index > first_char_index and text not in ['.', ',', ';', ':']:
                    text_block_entries.append(' ')
                text_block_entries.append(str(text))
                confidence_entries.append(conf)

    avg_confidence = sum(confidence_entries) / len(confidence_entries) / 100.0

    return {
        'result': ''.join(text_block_entries),
        'confidence': avg_confidence
    }