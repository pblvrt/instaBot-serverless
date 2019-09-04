import json
from Instagram import InstagramAPI
import time, random, os, sys
import boto3
from boto3.dynamodb.conditions import  Key

dynamoClient = boto3.resource('dynamodb')
table = dynamoClient.Table('instaTable')
scannedTable = dynamoClient.Table('scannedTable')

def instaBot(event, context):

    username = os.environ['username']
    password = os.environ['password']
    hashtags = os.environ['hashtags'].split('|')

    api = InstagramAPI(username, password)
    api.login()
    api.searchUsers(random.choice(hashtags))  # get self user feed

    for user in api.LastJson['users']:
        response = scannedTable.get_item(
            Key={
                'username': user['username'], 'pk': user['pk']
            }
        )
        try:
            print(response['Item'])
        except KeyError:
            scannedTable.put_item(Item=user)
            api.getUserFollowers(user['pk'], maxid = '')
            for follower in api.LastJson['users']:
                print(follower)
                try:
                    table.put_item(Item=follower)
                except:
                    pass
            return
