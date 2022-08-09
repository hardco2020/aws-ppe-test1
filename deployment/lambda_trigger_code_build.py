import boto3

def lambda_handler(event, context):
    client = boto3.client('codebuild')
    env_var=[
        {
            'name': 'TASK_TOKEN',
            'value': event['token'],
            'type': 'PLAINTEXT'
        },
        {
            'name': 'MODEL_S3',
            'value': event['otherInput']['model_data_url'],
            'type': 'PLAINTEXT'
        }
    ]
    build = client.start_build(projectName='build-panorama-app', environmentVariablesOverride=env_var)
    build_id = build['build']['id']
    return {
        'statusCode': 200,
        'build_id': build_id,
    }
