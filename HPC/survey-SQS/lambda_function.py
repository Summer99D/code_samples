import json
import boto3
from decimal import Decimal

# Initialize boto3 clients with explicit region
s3_client = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    # Process all records in the SQS event
    for sqs_record in event['Records']:
        record = json.loads(sqs_record['body'])

        # Validate time_elapsed
        if record.get('time_elapsed', 0) < 3:
            continue  # Skip this record, process the next one

        # Write to S3
        user_id = record['user_id']
        timestamp = record['timestamp']
        object_key = f"{user_id}{timestamp}.json"
        try:
            s3_client.put_object(
                Bucket='hw05-summer99d',
                Key=object_key,
                Body=json.dumps(record, default=str),
                ContentType='application/json'
            )
        except Exception as e:
            print(f"Error writing to S3: {e}")
            raise

        # Write to DynamoDB
        table = dynamodb.Table('SurveyResponses_Summer99D_HW06')
        user_records = table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )['Items']
        num_submission = len(user_records) + 1

        try:
            table.put_item(
                Item={
                    'user_id': user_id,
                    'timestamp': timestamp,
                    'q1': Decimal(str(record.get('q1', 0))),
                    'q2': Decimal(str(record.get('q2', 0))),
                    'q3': Decimal(str(record.get('q3', 0))),
                    'q4': Decimal(str(record.get('q4', 0))),
                    'q5': Decimal(str(record.get('q5', 0))),
                    'freetext': record.get('freetext', ''),
                    'num_submission': Decimal(str(num_submission))
                }
            )
        except Exception as e:
            print(f"Error writing to DynamoDB: {e}")
            raise

    return {'statusCode': 200}