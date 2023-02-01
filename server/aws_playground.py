import boto3
s3_client = boto3.client("s3")
# secret key - 2VtKdP1PHKh3dAbdjt9X+jIFr4+TAEULdoHmHiiP
# access - AKIA4TY6Y5CRV7VPBSMD
s3 = boto3.client('s3', aws_access_key_id='AKIA4TY6Y5CRV7VPBSMD',aws_secret_access_key='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')
response = s3.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]
print("Bucket List: %s" % buckets)