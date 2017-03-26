#!/usr/bin/env python
import boto3, os

bucket = 'laszlo-szoboszlai'
s3 = boto3.resource('s3')

def list_bucket(bucket_name):
    bucket = s3.Bucket(bucket_name)
    filenames = []
    for obj in bucket.objects.all():
        filenames.append(obj.key)
    return filenames

# Print out bucket names
def list_buckets():
    for bucket in s3.buckets.all():
        print(bucket.name)

def list_pwd():
    filenames = []
    for file in os.listdir('.'):
        filenames.append(file)
    return filenames

#returns A-B = the elements are not in B but in A
def getdiff(listA, listB):
    return [item for item in listA if item not in listB]


# Upload a new file into a bucket
def upload(bucket, file):
    s3.Bucket(bucket).put_object(Key= file, Body=open(file, 'rb'))


#uploads all different files in pwd
def upload_all_diff(bucket):
    diffs = getdiff(list_pwd(), list_bucket(bucket))
    diffs.remove('.idea')
    diffs.remove('.git')
    counter = 0
    for diff in diffs:
        upload(bucket,diff)
        counter+=1
    return counter

def download(bucket_name, file):
    bucket = s3.Bucket(bucket_name)

    body = bucket.Object(file).get()['Body']
    with open(file, 'wb') as data:
        for chunk in iter(lambda: body.read(4096), b''):
            data.write(chunk)

def download_all_diff(bucket):
    diffs = getdiff(list_bucket(bucket), list_pwd())

    counter = 0
    for diff in diffs:
        download(bucket, diff)
        counter += 1
    return counter

def sync_all():
    return upload_all_diff(bucket), download_all_diff(bucket)

def main():
    up, down = sync_all()
    print('{} file(s) synced, {}▲ / {}▼ .'.format(up+down, up, down))
    pass

if __name__ == "__main__":
    main()