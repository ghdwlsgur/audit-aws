# import datetime
import os
import requests
import json


SLACK_WEBHOOK = os.environ['SLACK_WEBHOOK']


def lambda_handler(event, context):
    data = event['detail']
    user_identity = data['userIdentity']
    event_time = data['eventTime']
    group = user_identity['arn'].split("/")[1].split("_")[1]
    user = user_identity['arn'].split("/")[2]
    event_id = data['eventID']
    event_source = data['eventSource']
    event_name = data['eventName']
    aws_region = data['awsRegion']
    client_ip = data['sourceIPAddress']
    request_parameters = data['requestParameters']

    text = f"{user}님이 {client_ip}에서 {event_name}을(를) 수행했습니다."
    message_blocks = [
        {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": f"*{text}*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Event ID:*\n```{event_id}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Event Source:*\n```{event_source}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Event Name:*\n```{event_name}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*AWS Region:*\n```{aws_region}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Client IP:*\n```{client_ip}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Event Time:*\n```{event_time}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*User Group:*\n```{group}```"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*User:*\n```{user}```"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": f"*Request Parameters:*\n```{json.dumps(request_parameters, indent=2)}```"
            }
        }
    ]

    try:
        payload = {
            "blocks": message_blocks
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(
            SLACK_WEBHOOK,
            data=json.dumps(payload),
            headers=headers)

        # Logging response for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")

        return {
            'statusCode': response.status_code,
            'body': response.text
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
