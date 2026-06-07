import json
import boto3

ses = boto3.client('ses', region_name='eu-north-1')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        message = body['message']

        ses.send_email(
            Source='aliahmed96515@hotmail.com',
            Destination={
                'ToAddresses': ['aliahmed96515@hotmail.com']
            },
            Message={
                'Subject': {
                    'Data': f'CV Contact Form - Message from {name}'
                },
                'Body': {
                    'Text': {
                        'Data': f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
                    }
                }
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'message': 'Email sent successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }