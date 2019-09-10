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

    RandomItem = usersTable.scan(
        ProjectionExpression = "username"
    )
    randomUser = random.choice(RandomItem['Items'])['username']

    response = usersTable.query(
        KeyConditionExpression=Key('username').eq(randomUser)
    )
    #print(response['Items'][0]['pk'])
    account = accountTable.get_item(
        Key={
        'date': str(datetime.datetime.now().date()), 'username': username
        }
    )
    #print(account)
 
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
    
    if account['Item']['followed'] >= int(os.environ['rateLimitsFollow']):
        return
    else:
        
        api = InstagramAPI(username, password)
        api.login()
        print(api.follow(int(response['Items'][0]['pk'])))
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
        