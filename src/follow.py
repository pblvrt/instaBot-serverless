import json
from Instagram import InstagramAPI
import time, random, os, sys, datetime
import boto3
from boto3.dynamodb.conditions import Key

dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table(os.environ['accountTable'])
scannedTable = dynamoClient.Table(os.environ['scannedTable'])
usersTable = dynamoClient.Table(os.environ['usersTable'])

def follow(event, context):
    username = os.environ['username']
    password = os.environ['password']

    # Check current user, if not exists create it
    account = accountTable.get_item(
        Key={
        'date': str(datetime.datetime.now().date()), 'username': username
        }
    ) 
    try:
        test = account['Item']
    except KeyError:
        Item = {
            'date': str(datetime.datetime.now().date()),
            'username': username,
            'followed': 0,
            'comments': 0,
            'unfollowed': 0,
            'likes': 0,
            'blocked': 'False'
        }
        accountTable.put_item(Item=Item)
        return
    
    # Check if we are over rate limits stipulated in serverless.yml
    if account['Item']['followed'] <= int(os.environ['rateLimitsFollow']):
        # login
        api = InstagramAPI(username, password)
        api.login()

        # Get random user from followers of users defined in serverless.yml
        randomUser = get_random_user(api)
        if randomUser not None:
            # Check user doesent exist.
            response = usersTable.query(
                KeyConditionExpression=Key('username').eq(user['username'])
            )
            try:
                print(response['Items'][0]['pk'])
            except IndexError:
                follow = Follower(randomUser, api, os.environ['tags'].split("|"), os.environ['users'].split("|"))


        response = usersTable.update_item(
            Key={
                'username': randomUser, 'pk': response['Items'][0]['pk']
            },
            AttributeUpdates={
                'followed': {
                    'Value': True,
                    'Action': 'PUT'
                },
                'followed_date': {
                    'Value': str(datetime.datetime.now().date()),
                    'Action': 'PUT'
                }
            }
        )
        

        # Update table account +1 follow count
        reply = accountTable.update_item(
            Key={
                'date': str(datetime.datetime.now().date()), 'username': username
            },
            AttributeUpdates={
                'followed': {
                    'Value': 1,
                    'Action': 'ADD'
                }
            }
        )
        
def get_random_user(api):
    user = os.environ['users'].split("|")
    self.api.searchUsers(user)
    try:
        api.getUserFollowers(api.LastJson['users'][0]['pk'])
        json_user = random.choice(api.LastJson['users'])
    except:
        return None
    return json_user