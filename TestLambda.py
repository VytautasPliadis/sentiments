import boto3
import json
from translate import Translator
from textblob import TextBlob


class LithuanianToEnglishTranslator:
    def __init__(self):
        self.translator = Translator(to_lang="en", from_lang="lt")

    def translate_list(self, lithuanian_words):
        english_words = []
        for word in lithuanian_words:
            translation = self.translator.translate(word)
            english_words.append(translation)
        return english_words


class SentenceTranslator:
    def __init__(self, source_lang="lt", target_lang="en"):
        self.translator = Translator
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate_sentence(self, sentence):
        translation = self.translator.translate(sentence, src=self.source_lang, dest=self.target_lang)
        return translation.text

    def translate_sentences(self, sentences):
        translated_sentences = []
        for sentence in sentences:
            translated_sentence = self.translate_sentence(sentence)
            translated_sentences.append(translated_sentence)
        return translated_sentences


# Define a function to calculate sentiment polarity for a given dictionary key
def get_sentiment(data, key, translator):
    titles_lt = data.get(key, '')
    titles_en = translator.translate_list(titles_lt)
    text = '. '.join(titles_en)
    print(text)
    blob = TextBlob(text)
    sentiment = round(blob.sentiment.polarity, 2)
    return str(sentiment)


def lambda_handler(event, context):
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table_name = 'sentiments'  # Replace with your DynamoDB table name
    table = dynamodb.Table(table_name)

    lt_translator = LithuanianToEnglishTranslator()

    # Replace 'your_queue_url' with the URL of your SQS queue
    queue_url = 'https://sqs.eu-north-1.amazonaws.com/806923321122/Lt_titles_scraped'

    # Initialize the SQS client
    sqs = boto3.client('sqs')

    try:
        # Receive a message from the SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'All'
            ],
            MessageAttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,  # Change this value if you want to receive more than one message at a time
            VisibilityTimeout=0,  # 0 seconds means the message will become available immediately
            WaitTimeSeconds=0  # Adjust this value if you want to enable long polling
        )

        # Check if there are messages in the response
        if 'Messages' in response:
            for message in response['Messages']:
                # Process the message content here
                # You can access the message body using message['Body']
                data = json.loads(message['Body'])
                sort_key = data['sort_key']

                # Define your dictionary keys and their corresponding variables
                keys = ['titles_lrt_lt', 'titles_delfi_lt', 'titles_15min_lt']

                # Calculate sentiment polarity for each key using the function
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

                except Exception as e:
                    return {
                        'statusCode': 500,
                        'body': json.dumps(f'Error: {str(e)}')
                    }

                # Delete the message from the queue
                receipt_handle = message['ReceiptHandle']
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )

        else:
            return {
                'statusCode': 200,
                'body': 'No messages in the queue.'
            }

            return {
                'statusCode': 200,
                'body': 'Message processed and deleted successfully. Data written to DynamoDB successfully!'
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
