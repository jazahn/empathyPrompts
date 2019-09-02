import os
import boto3
import random
from botocore.vendored import requests

import json
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('empathyprompts')


def formatMarkdown(markdown):
    # slack is stupid with their markdown, they decided to do their own limited markdown, and still call it mrkdwn
    result = re.sub(r'\[(.*?)\]\((.*?)\)', "<\\2|\\1>", markdown)
    result = re.sub('&#8217;', "'", result)
    result = re.sub('\n', "", result)
    return result

    
def lambda_handler(event, context):

    response = table.scan()
    items = response['Items']
    
    item = items[random.randint(0, len(items) - 1)]
    
    print(item)
    
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*"+item['title']+"*"
            }
        },
        {
    		"type": "divider"
    	},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": formatMarkdown(item['description'])
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_"+formatMarkdown(item['example'])+"_"
            }
        },
    	{
    		"type": "context",
    		"elements": [
    			{
    				"type": "mrkdwn",
    				"text": "All items taken from: <https://empathyprompts.net|empathyprompts.net>"
    			}
    		]
    	}
    ]
    
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token = os.environ.get('token')
    payload = {
        'channel': '#sewg',
        #'text': 'something',
        'blocks': json.dumps(blocks),
        'token': token,
        #'as_user': True
        'username': 'Empathy Prompts',
        'icon_url': 'https://img.icons8.com/cotton/64/000000/like--v5.png'
    }
    
    if 'title' in item:
        response = requests.post(url, payload, headers=headers)
        print(response)


    return {
        'statusCode': 200,
        'body': json.dumps('Happy happy, joy joy')
    }

