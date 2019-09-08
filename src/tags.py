import json
from Instagram import InstagramAPI
import time, random, os, sys
import boto3
from boto3.dynamodb.conditions import  Key
import datetime, time

dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table(os.environ['accountTable'])
scannedTable = dynamoClient.Table(os.environ['scannedTable'])
usersTable = dynamoClient.Table(os.environ['usersTable'])

def tags(event, context):

    username = os.environ['username']
    password = os.environ['password']
    hashtags = os.environ['hashtags'].split('|')
    randomHash = random.choice(hashtags)

    # login
    api = InstagramAPI(username, password)
    api.login()
    
    # search tags
    api.searchTags(randomHash)
    tagArray = api.LastJson['results']
    i = 0
    for tag in tagArray:
        api.getHashtagFeed(tag['name'])
        #print(json.dumps(api.LastJson, indent=4))
        for photo in api.LastJson['ranked_items']:            
            api.getMediaLikers(photo['id'])
            for liker in api.LastJson['users']:
                Item = {
                    'pk': liker['pk'],
                    'username': liker['username'],
                    'full_name': liker['full_name'],
                    'is_private': liker['is_private'],
                    'followed': False,
                    'followed_date': None
                }
                try:
                    usersTable.put_item(Item=Item)
                except Exception as e:
                    pass
                #print(json.dumps(api.LastJson, indent=4))
        i+=1
        if i == 5:
            break
    
