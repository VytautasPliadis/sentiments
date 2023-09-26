import boto3
import json
from translate import Translator
from textblob import TextBlob

# Initialize resources outside the lambda handler for reuse
dynamodb = boto3.resource('dynamodb')
table_name = 'sentiments'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)
lt_translator = LithuanianToEnglishTranslator()


# Define your translator classes and sentiment analysis functions here

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.eu-north-1.amazonaws.com/806923321122/Lt_titles_scraped'

    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            VisibilityTimeout=30,  # Adjust as needed
            WaitTimeSeconds=0
        )

        if 'Messages' in response:
            for message in response['Messages']:
                data = json.loads(message['Body'])
                sort_key = data['sort_key']

                keys = ['titles_lrt_lt', 'titles_delfi_lt', 'titles_15min_lt']
                sentiments = {key: get_sentiment(data, key, lt_translator) for key in keys}

                # Access the sentiments using their respective keys
                lrt_sentiment = sentiments['titles_lrt_lt']
                delfi_sentiment = sentiments['titles_delfi_lt']
                _15min_sentiment = sentiments['titles_15min_lt']

                print(f'data: {sort_key}')
                print(f'lrt: {lrt_sentiment}')
                print(f'delfi: {delfi_sentiment}')
                print(f'15min: {_15min_sentiment}')

                try:
                    # Write data to DynamoDB
                    table.put_item(Item={'Diena': sort_key, 'lrt': lrt_sentiment, 'delfi': delfi_sentiment,
                                         'fifteen': _15min_sentiment, 'Data': data})

                    # Delete the message from the queue only if it was successfully processed
                    receipt_handle = message['ReceiptHandle']
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                except Exception as e:
                    # Log the error and continue processing other messages
                    print(f'Error processing message: {str(e)}')

        else:
            print('No messages in the queue.')

    except Exception as e:
        # Log the error and return a response
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }

    # Return a response indicating successful processing
    return {
        'statusCode': 200,
        'body': 'Message processed and deleted successfully. Data written to DynamoDB successfully!'
    }
