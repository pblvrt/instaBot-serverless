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

def users(event, context):

    username = os.environ['username']
    password = os.environ['password']
    hashtags = os.environ['users'].split('|')
    randomHash = random.choice(hashtags)

    # login
    api = InstagramAPI(username, password)
    api.login()

    # search users
    api.searchUsers(randomHash)  

    for user in api.LastJson['hashtags']:
        response = scannedTable.get_item(
            Key={
                'username': user['username'], 'pk': user['pk']
            }
        )
        try:
        except KeyError:
            scannedTable.put_item(Item=user)
            next_max_id = True
            while next_max_id:
                
                # first iteration hack
                if next_max_id is True:
                    next_max_id = ''
                    _ = api.getUserFollowers(user['pk'], maxid=next_max_id)
                for follower in api.LastJson['users']:
                    try:
                        Item = {
                            'pk': liker['pk'],
                            'username': liker['username'],
                            'full_name': liker['full_name'],
                            'is_private': liker['is_private'],
                            'followed': False,
                            'followed_date': None
                        }
                        usersTable.put_item(Item=Item)
                    except:
                        pass
                next_max_id = api.LastJson.get('next_max_id', '')
            return
