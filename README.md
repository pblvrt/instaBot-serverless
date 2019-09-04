# InstaBot-serverless

This repo uses [InstragramAPI](https://github.com/LevPasha/Instagram-API-python) to call the unofficial instagram api.

### Installing:
* You will need to install [serverless framework](https://serverless.com/).
* Clone this repo and `npm install`and `pip instal -r requirements.txt` .
* Fill out serverless.yml env variables with instagram credentials.
* `sls deploy` to deploy this service to the aws cloud.

### Resources being deployed:
* 3 Dynamodb tables.
* 5 Lambda functions.
* IAM role statement, allow all dynamodb actions on specified tables.

### What the bot does:
1. Based on the hashtags supplied in serverless.yaml, the bot will scan those hashtags and add user accounts interacting with them to database. 
2. There are 5 different functions available:
  - Follow: It will follow a random user in the database.
  - Unfollow: It will unfollow a random user that you follow; You can set `unfollowAll` in serverless.yaml to 'False' so that the bot wont unfollow people that follow you.
  - Comment: The bot will comment a random picture of a random user in the database.
  - Like: The bot will like a random picture of a random user in the database.
  - Repost: This function will repost a random photo of a random user related to the hashtags specified.
3. Default invocations rates have been set to the functions, this rates have worked for me personally in regards to not getting banned. You can adjust the rates in the serverless.yaml file.

### Disclaimer:
Im not responsable for any consecuences you may be subjected to while using this  software.
