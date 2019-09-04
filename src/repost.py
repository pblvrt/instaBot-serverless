from time import sleep
import requests
import urllib
import os
import json
import urllib.request
import boto3
import random
import shutil
from Instagram import InstagramAPI

dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table(os.environ['accountTable'])
scannedTable = dynamoClient.Table(os.environ['scannedTable'])
usersTable = dynamoClient.Table(os.environ['usersTable'])

def repost(event, context):

    username = os.environ['username']
    password = os.environ['password']

    RandomItem = scannedTable.scan(
        ProjectionExpression = "username"
    )
    print(random.choice(RandomItem['Items'])['username'])

    request_url = "https://www.instagram.com/" + random.choice(RandomItem['Items'])['username'] + "?__a=1"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    response = requests.get(request_url, headers=headers)
    node = random.choice(response.json()['graphql']['user']['edge_owner_to_timeline_media']['edges'])
    caption = node['node']['edge_media_to_caption']['edges'][0]['node']['text']
    fileUrl = node['node']['display_url']

    r = requests.get(fileUrl, stream=True)
    if r.status_code == 200:
        with open('/tmp/test.jpg', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f) 

    api = InstagramAPI(username, password)
    api.login()
    api.uploadPhoto('/tmp/test.jpg', caption=caption, upload_id=None, is_sidecar=None)