import json
import boto3

ses = boto3.client('ses', region_name='eu-north-1')

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST,OPTIONS'
}

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': ''
        }

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
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': 'Email sent successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }