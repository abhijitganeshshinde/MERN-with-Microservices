import boto3
import datetime
import pymongo
from bson.json_util import dumps

def lambda_handler(event, context):
    # MongoDB connection details
    mongo_uri = "mongodb+srv://xyz:abcd@cluster0.bta0sbt.mongodb.net/microservice"  # Replace with your MongoDB connection details
    client = pymongo.MongoClient(mongo_uri)
    db = client.get_database()

    # Generate timestamp for backup file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    # Backup MongoDB data
    backup_data = dumps(db.collection.find())  # Perform the backup based on your MongoDB schema and requirements

    # Store backup in S3 bucket
    s3 = boto3.client('s3')
    bucket_name = 'mongodbbackup-abhi'
    key = f'mongodb_backups/backup_{timestamp}.json'  # Example key structure for backup file

    # Upload backup data to S3
    s3.put_object(Body=backup_data, Bucket=bucket_name, Key=key)

    return {
        'statusCode': 200,
        'body': f'MongoDB Backup created and stored in S3 at {key}'
    }
