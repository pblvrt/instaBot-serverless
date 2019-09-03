import json
from InstagramAPI import InstagramAPI
import time, random, os, sys
import boto3
from boto3.dynamodb.conditions import  Key

dynamoClient = boto3.resource('dynamodb')
table = dynamoClient.Table('instaTable')
table2 = dynamoClient.Table('scannedTable')

def instaBot(event, context):

    api = InstagramAPI("npmScripts", "npmScripts8611")
    api.login()

    hastags = ["coding", "programador", "robots", "ordenadores", "coder" ]

    api.searchUsers(random.choice(hastags))  # get self user feed

    time.sleep(random.randint(1, 10))

    for user in api.LastJson['users']:
        print(user)

        response = table2.get_item(
            Key={
                'username': user['username'], 'pk': user['pk']
            }
        )
        print(response)
        
        try:
            print(response['Item'])
        except KeyError:
            table2.put_item(Item=user)
            api.getUserFollowers(user['pk'], maxid = '')
            for follower in api.LastJson['users']:
                print(follower)
                try:
                    table.put_item(Item=follower)
                except:
                    pass
            return