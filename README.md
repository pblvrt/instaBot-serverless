# InstaBot-serverless

This repo uses [InstragramAPI](https://github.com/LevPasha/Instagram-API-python) to call the unoficial instagram api.

### Installing:
* You will need to install serverless framework[https://serverless.com/].
* Clone this repo and `npm install`and `pip instal -r requirements.txt` .
* Fill out serverless.yml env variabels with instagram credentials.
* `sls deploy` to deploy this service to the aws cloud.

### Resources beeing deployed:
* 3 Dynamodb tables.
* 5 Lambda functions.
* IAM role statement, allow all dynamodb actions on specified tables.

### What the bot does:

