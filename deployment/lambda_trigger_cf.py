import json
import logging
import boto3
from botocore.exceptions import ClientError
from datetime import datetime


def download_yaml(bucket_name, object_name, filename):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.download_file(bucket_name, object_name, filename)
    except ClientError as e:
        logging.error(e)
        
def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('cloudformation')
    cf_filename = "/tmp/my_cf_template.yaml"
    stackname = "PackageMyApp"+str(datetime.timestamp(datetime.now())).split(".")[0]
    download_yaml('cf-templates-w15klxracsc-ap-southeast-1', 'create_app_cf_template.yaml', cf_filename)
    
    with open(cf_filename, 'r') as cf_file:
        cf_template = cf_file.read()
        cf_template = cf_template.replace("token_to_be_modified", event['token'])
        response = client.create_stack(
            StackName=stackname,
            TemplateBody=cf_template,
            Capabilities=['CAPABILITY_IAM']
        )
    
    # while client.describe_stacks(StackName=stackname)["Stacks"][0]["StackStatus"]!="CREATE_COMPLETE":
    #     print("creation in progress ...")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'stackName': stackname
    }
