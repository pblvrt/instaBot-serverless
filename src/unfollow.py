import json
from Instagram import InstagramAPI
import time, random, os, sys, datetime
import boto3

dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table('accountTable')
instaTable = dynamoClient.Table('instaTable')

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
        user = random.choice(api.LastJson['users'])['pk']
        #user = '4808870069'
        if str(os.environ['unfollowAll']) == 'False':
            api.userFriendship(user)
            if(api.LastJson['followed_by']):
                return  
        api.unfollow(user)
        print(api.LastJson)
        print("FOLLOWINGS=================")
        api.getSelfUsersFollowing()
        print(len(api.LastJson['users']))
        print("FOLLOWERS=================")
        api.getSelfUserFollowers()
        print(len(api.LastJson['users']))
        response = accountTable.update_item(
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