import requests
import boto3
import logging

from botocore.exceptions import ClientError
from chalice import Chalice

app = Chalice(app_name='presigned-url', debug=True, configure_logs=False)
# Logging
app.debug = True
logging.getLogger().setLevel(logging.DEBUG)

s3_client = boto3.client('s3', region_name="ap-south-1", aws_access_key_id="",
                         aws_secret_access_key="7UMxL4Y9VxgJPgzxXudDm1jUoZb7YHf0aT1XtNuO")
bucket = "evoters.in"


# @app.route('/generate-pre-signed-url-for-upload', methods=['POST'], content_types=['application/json'])
# def generate_pre_signed_url_for_upload():
#     logging.debug("Generate Pre-Signed URL for upload")
#     request = app.current_request
#     data = request.json_body
#     response = get_pre_signed_url(data['file_name'])
#     files = {'file': open("/Users/thirumal/Downloads/ACC.png", 'rb')}
#     print(files)
#     http_response = requests.post(response['url'], data=response['fields'], files=files)
#     print(http_response)
#     # If successful, returns HTTP status code 204
#     logging.info(f'File upload HTTP status code: {http_response.text}')
#     return response


@app.lambda_function()
def handler(event, context):
    logging.debug(event)
    return get_pre_signed_url(event['arguments']['fileName'])


def get_pre_signed_url(file_name):
    try:
        response = s3_client \
            .generate_presigned_post(Bucket=bucket, Key=file_name, ExpiresIn=300)
    except ClientError as e:
        logging.error(e)
        return None
    logging.debug("Pre-Signed URL {}".format(response))
    print(response)
    return response
