import unittestimport jsonimport boto3from MontyCloud.app.list_image import ListImagefrom MontyCloud.app.image_upload import UploadImagefrom MontyCloud.app.download_image import DownloadViewImagefrom MontyCloud.app.delete_image import DeleteImage# from moto import mock_s3, mock_dynamodb2TEST_S3_BUCKET_NAME = "test-image"TEST_DYNAMODB_TABLE = "test-table"ENDPOINT_URL = "http://localhost.localstack.cloud:4566"class TestUploadImageLambda(unittest.TestCase):    # @mock_s3    # @mock_dynamodb2    # def setUp(self):    #     self.s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL)    #     self.dynamodb_client = boto3.client('dynamodb', endpoint_url=ENDPOINT_URL)    #    #     # Create mock S3 bucket    #     self.s3_client.create_bucket(Bucket='test-bucket')    #    #     # Create mock DynamoDB table    #     self.dynamodb_client.create_table(    #         TableName='test-table',    #         KeySchema=[    #             {'AttributeName': 'id', 'KeyType': 'HASH'}    #         ],    #         AttributeDefinitions=[    #             {'AttributeName': 'id', 'AttributeType': 'S'}    #         ],    #         ProvisionedThroughput={    #             'ReadCapacityUnits': 10,    #             'WriteCapacityUnits': 10    #         }    #     )    def test_upload_image(self):        # Mock event data for Lambda function        event = {            'resource': 'upload_image',            'body': json.dumps({                'title': 'Test Image',                'description': 'Test image description',                'tags': ['test', 'image'],                'imageFile': 'dummy-image-data'  # Replace with actual image data            })        }        # Invoke Lambda function        response = UploadImage(event, {})        print(response)        # Assert Lambda function response        self.assertEqual(response['statusCode'], 200)        self.assertIn('imageId', json.loads(response['body']))        self.assertEqual(json.loads(response['body'])['message'], 'Image uploaded successfully')    def test_list_images(self):        # Mock event data for Lambda function (no filters)        event = {}        # Invoke Lambda function        response = ListImage(event, {})        # Assert Lambda function response        self.assertEqual(response['statusCode'], 200)        images = json.loads(response['body'])        self.assertIsInstance(images, list)    def test_view_image(self):        # Mock event data for Lambda function        event = {            'pathParameters': {'imageId': 'test-image-id'}        }        # Invoke Lambda function        response = DownloadViewImage(event, {})        # Assert Lambda function response        self.assertEqual(response['statusCode'], 200)        data = json.loads(response['body'])        self.assertIn('presignedUrl', data)    def test_delete_image(self):        # Mock event data for Lambda function        event = {            'pathParameters': {'imageId': 'test-image-id'}        }        # Invoke Lambda function        response = DeleteImage(event, {})        # Assert Lambda function response        self.assertEqual(response['statusCode'], 200)        self.assertEqual(json.loads(response['body'])['message'], 'Image deleted successfully')