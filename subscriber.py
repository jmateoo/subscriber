from flask import Flask, make_response, jsonify
import boto3, logging, time

app = Flask(__name__)


sqs = boto3.client('sqs', region_name='us-east-1')  
queue_url = 'https://sqs.us-east-1.amazonaws.com/019856031236/traslateoperator'  
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_sqs_messages():
    try:
        while True:  
            response = sqs.receive_message(QueueUrl=queue_url, AttributeNames=['All'])
            messages = response.get('Messages', [])

            if not messages:
                print("No messages in the queue. Listening...")
                time.sleep(5)  
                continue 

            for message in messages:
                try:
                    print("Message received:", message['Body'])
                    
                    receipt_handle = message['ReceiptHandle']
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                    print("Message processed successfully.")
                except Exception as e:
                    print("Error in message processing:", str(e))

    except Exception as e:
        print("Error:", str(e))

process_sqs_messages()

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({"message": "Failed: Application Error.."}), 500)

@app.errorhandler(501)
def not_implemented(error):
    return make_response(jsonify({"message": "Failed: Wrong Parameters.."}), 501)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
