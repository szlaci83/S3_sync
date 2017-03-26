#!/usr/bin/env python
import boto3, os

bucket = 'laszlo-szoboszlai'
s3 = boto3.resource('s3')

def list_bucket(bucket_name):
    bucket = s3.Bucket(bucket_name)
    filenames = []
    for obj in bucket.objects.all():
        #print(obj.key)
        filenames.append(obj.key)
    return filenames

# Print out bucket names
def list_buckets():
    for bucket in s3.buckets.all():
        print(bucket.name)

def list_pwd():
    path = '.'
    files = os.listdir(path)
    filenames = []
    for file in files:
        #print(file)
        filenames.append(file)
    return filenames

#returns A-B = the elements are not in B but in A
def getdiff(listA, listB):
    result = [item for item in listA if item not in listB]
    return result

# Upload a new file into a bucket
def upload(bucket, file):
    data = open(file, 'rb')
    s3.Bucket(bucket).put_object(Key= file, Body=data)


#uploads all different files in pwd
def upload_all_diff(bucket):
    files_in_pwd = list_pwd()
    files_in_bucket = list_bucket(bucket)
    diffs = getdiff(files_in_pwd, files_in_bucket)
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
    files_in_pwd = list_pwd()
    files_in_bucket = list_bucket(bucket)
    diffs = getdiff(files_in_bucket, files_in_pwd)

    counter = 0
    for diff in diffs:
        download(bucket, diff)
        counter += 1
    return counter

def sync_all():
    up = upload_all_diff(bucket)
    down = download_all_diff(bucket)
    return up, down

def main():
    #print('{} file(s) uploaded.'.format(upload_all_diff(bucket)))
    #print(list_bucket(bucket))
    # print(list_pwd())
    #print('{} file(s) downloaded.'.format(download_all_diff(bucket)))
    up, down = sync_all()
    print('{} file(s) synced, {}▲ / {}▼ .'.format(up+down, up, down))
    pass
if __name__ == "__main__":
    main()