import jsonfrom MontyCloud.app.image import Imagesfrom MontyCloud.utils.logger import loggerclass DeleteImage(Images):    def __init__(self, event, context):        super().__init__()        self.event = event        self.context = context    def perform_task(self):        try:            # Extract path parameter from API Gateway event            image_id = self.event['pathParameters']['imageId']            # Query DynamoDB for metadata            response = self.dynamodb_client.get_item(                TableName=self.table_name,                Key={'imageId': {'S': image_id}}            )            # Check if item exists            if 'Item' not in response:                return {                    'statusCode': 404,                    'body': json.dumps({'error': 'Image not found'})                }            # Retrieve S3 object key from metadata            s3_object_key = f"{image_id}.jpg"  # Example: Assuming object key is based on imageId            # Delete image file from S3            self.s3_client.delete_object(Bucket=self.s3_bucket, Key=s3_object_key)            # Delete metadata from DynamoDB            self.dynamodb_client.delete_item(                TableName=self.table_name,                Key={'imageId': {'S': image_id}}            )            # Return success response            response = {                'statusCode': 204,                'body': json.dumps({'message': 'Image deleted successfully', 'imageId': image_id})            }        except Exception as err:            logger.error(f"Delete image failed, Error: {err}")            # Return error response            response = {                "statusCode": 500,                "body": json.dumps({                    "message": "Delete image failed.",                    "error": str(err)})            }        return response