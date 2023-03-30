import boto3

def s3_reader(bucket:str,file:str) -> list:
    s3 = boto3.resource('s3')

    s3_object = s3.Bucket(bucket).Object(file).get()
    res = s3_object['Body'].read().decode()

    clean_res = res.split('\n')

    return clean_res

if __name__=="__main__":
    print(s3_reader('gw2-srs-bucket','urls.txt'))