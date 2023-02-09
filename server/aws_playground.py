import boto3
import io
from pathlib import Path
s3_client = boto3.client("s3")

# secret key - 2VtKdP1PHKh3dAbdjt9X+jIFr4+TAEULdoHmHiiP
# access - AKIA4TY6Y5CRV7VPBSMD
s3 = boto3.client('s3', aws_access_key_id='AKIA4TY6Y5CRV7VPBSMD', aws_secret_access_key='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')
# response = s3.list_buckets()
# buckets = [bucket['Name'] for bucket in response['Buckets']]
# print("Bucket List: %s" % buckets)
image = Path('/Users/zhenyabudnyk/Documents/myProjects/mood-board-search/backend/static-cav-content/jpgs/9fcd45d92a07cdb7e6b7d8678a520293.1x.1200x1200.jpg')

s3.upload_file(str(image), 'brief-project-for-cm', 'designer-view/photo1.jpg')
# with open(image, 'rb') as data:
#     # file = io.BytesIO(data.read())
#     s3.upload_file('designer-view/photo1.jpg', 'brief-project-for-cm', file)
    # moodboard['urls'][uuid.uuid4().hex] = s3.generate_presigned_url(
    # ClientMethod='get_object',
    # Params={
    #     'Bucket': 'brief-project-for-cm',
    #     'Key': 'designer-view/' + str(image)
    # }, )

