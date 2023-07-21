import boto3
def read_email_ids_from_s3(bucket_name, file_name):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, file_name)
    email_ids = obj.get()['Body'].read().decode('utf-8').split('\n')
    return [email_id.strip() for email_id in email_ids if email_id.strip()]
def send_email(email_id):
    ses = boto3.client('ses', region_name='ap-south-1')  # Change the region to your desired SES region
    sender_email = 'aaryangupta2201@gmail.com'  # Replace with your SES-verified sender email
    subject = 'Alert !, new data uploded in s3'
    body = 'Alert email from aws , new data is there in s3 bucket_name.'
    
    response = ses.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [email_id]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )
    
    print(f"Email sent to {email_id}. Message ID: {response['MessageId']}")
def lambda_handler(event, context):
    # Replace 'your-bucket-name' and 'email_ids.txt' with your S3 bucket and file name
    bucket_name = 'lwtask5'
    file_name = 'emails.txt'
    
    email_ids = read_email_ids_from_s3(bucket_name, file_name)
    
    for email_id in email_ids:
        send_email(email_id)

    return {
        'statusCode': 200,
        'body': 'Emails sent successfully!'
    }
