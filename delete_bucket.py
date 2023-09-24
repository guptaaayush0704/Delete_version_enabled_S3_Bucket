from concurrent.futures import ThreadPoolExecutor
import boto3

client = boto3.client(
    "s3",
    aws_access_key_id='',
    aws_secret_access_key=''
)

bucketname = 'bucket_name'

def deleteobjects(key, versionid):
    response = client.delete_object(Bucket=bucketname, Key=key, VersionId=versionid)
    print('Deleting object {0} for version {1}'.format(key, versionid))

#We will need to gather a list of all versions by using the paginator for the list_object_versions call
paginator = client.get_paginator('list_object_versions')
pages = paginator.paginate(Bucket=bucketname) #Removed the Prefix parameter to target the entire bucket
for page in pages:

    listofversions = page.get('Versions')
    #print(listofversions)
    if listofversions != None:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for object in listofversions:
                executor.submit(deleteobjects, key=object['Key'], versionid=object['VersionId'])

print('Deletion complete!')