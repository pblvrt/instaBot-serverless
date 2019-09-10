import json
from Instagram import InstagramAPI
import time, random, os, sys, datetime
import boto3
from boto3.dynamodb.conditions import Attr, Key

dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table(os.environ['accountTable'])
scannedTable = dynamoClient.Table(os.environ['scannedTable'])
usersTable = dynamoClient.Table(os.environ['usersTable'])

def unfollow(event, context):
    username = os.environ['username']
    password = os.environ['password']

    account = accountTable.get_item(
        Key={
        'date': str(datetime.datetime.now().date()), 'username': username
        }
    ) 
    try:
        print(account['Item'])
    except KeyError:
        Item = {
            'date': str(datetime.datetime.now().date()),
            'username': username,
            'followed': 0,
            'comments': 0,
            'unfollowed': 0,
            'likes': 0,
            'blocked': False
        }
        accountTable.put_item(Item=Item)
        return
    
    if account['Item']['unfollowed'] >= int(os.environ['rateLimitsFollow']):
        return
    else:
        api = InstagramAPI(username, password)
        api.login()

        api.getSelfUsersFollowing()
        username = random.choice(api.LastJson['users'])['username']
        #user = '4808870069'
        user = usersTable.query(
            KeyConditionExpression=Key('username').eq('_anmolvirdi_')
        )
        try:
            print(user['Items'][0]['followed'])
            if str(os.environ['unfollowAll']) == 'False':
                api.userFriendship(user)
                if(api.LastJson['followed_by']):
                    return


            api.unfollow(user)
            response = accountTable.update_item(
                Key={
                    'date': str(datetime.datetime.now().date()), 'username': username
                },
                AttributeUpdates={
                    'unfollowed': {
                        'Value': 1,
                        'Action': 'ADD'
                    }
                }
            )
        except:
