import json
import time
import random
import os
import sys
import datetime
import boto3
from src.utils.Follower import Follower 
from boto3.dynamodb.conditions import Key
from Instagram import InstagramAPI

client = boto3.client('sqs')
dynamoClient = boto3.resource('dynamodb')
accountTable = dynamoClient.Table(os.environ['accountTable'])
scannedTable = dynamoClient.Table(os.environ['scannedTable'])
usersTable = dynamoClient.Table(os.environ['usersTable'])

def analyze_followers(event, context):
    # Getting params from os variables; defined in serverless.yml
    username = os.environ['username']
    password = os.environ['password']

    #login
    api = InstagramAPI(username, password)
    api.login()
  
    try:
        body = json.loads(event['Records'][0]['body'])
        next_max_id = body['next_max_id']
        print(next_max_id)
    except KeyError:
        next_max_id = ''
    
    try:
        response = client.delete_message(
            QueueUrl = os.environ['next_max_id_queue'],
            ReceiptHandle=event['Records'][0]['receiptHandle']
        )
    except:
        pass       

    if next_max_id == 'None':
        return

    # find current user by username
    try:
        api.searchUsers(username)  
        currentUser = api.LastJson['users'][0]
    except:
        print(api.searchUsers(username))
        print(api.LastJson)

    # loop through user followings
    try:
        _ = api.getUserFollowings(currentUser['pk'], maxid=next_max_id)
        users = api.LastJson['users']
    except:
        users = []
        
    # all items
    allItems = scannedTable.scan(ProjectionExpression = "pk")
    totalCount = 0
    count = 0
    for user in users:
        isInList = False
        if count == 10:
            break
        for item in allItems['Items']:
            if str(user['pk']) == str(item['pk']):
                totalCount +=1
                allItems['Items'].remove(item)
                isInList = True
        if not isInList:
            follow = Follower(user, api, os.environ['tags'].split("|"), os.environ['users'].split("|"))
            print(follow.get_user())
            response = scannedTable.put_item(Item=follow.get_user())
            count += 1
    
    print(totalCount)
    print(count)
    totalUsers = len(users)
    print(api.LastJson.get('next_max_id', ''))
    
    if totalCount == totalUsers:
        # Send message to queue with  nex_max_id
        try:
            response = client.send_message(
                QueueUrl = os.environ['next_max_id_queue'],
                MessageBody = json.dumps({"next_max_id": api.LastJson.get('next_max_id', '')})
            )
        except Exception as e:
            print(e)
    else:
        # Send message to queue with  nex_max_id
        try:
            response = client.send_message(
                QueueUrl = os.environ['next_max_id_queue'],
                MessageBody = json.dumps({"next_max_id": next_max_id})
            )
        except Exception as e:
            print(e)
