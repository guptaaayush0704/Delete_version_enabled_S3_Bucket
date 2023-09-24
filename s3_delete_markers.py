import boto3
from concurrent.futures import ThreadPoolExecutor

client = boto3.client(
    "s3",
    aws_access_key_id='',
    aws_secret_access_key=''
)

bucketname = 'bucket_name'

def deleteobjects(key, versionid):
    response = client.delete_object(Bucket=bucketname, Key=key, VersionId=versionid)
    print('Deleting delete marker {0} for version {1}'.format(key, versionid))

#We will need to gather a list of all versions by using the paginator for the list_object_versions call
paginator = client.get_paginator('list_object_versions')
pages = paginator.paginate(Bucket=bucketname) #Removed the Prefix parameter to target the entire bucket
for page in pages:
    listofdeletemarkers = page.get('DeleteMarkers')
    if listofdeletemarkers != None:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for deletemarker in listofdeletemarkers:
            	executor.submit(deleteobjects, key=deletemarker['Key'], versionid=deletemarker['VersionId'])

print('Deletion of delete markers complete!')
