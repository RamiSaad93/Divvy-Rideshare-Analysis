import boto3
from botocore import UNSIGNED
from botocore.config import Config


# Divvy public S3 bucket
source_bucket = "divvy-tripdata"

# My S3 bucket
destination_bucket = "divvy-bike-project-rami-865411539075-eu-central-1-an"

# Folder where the raw 2023 files will be stored
destination_prefix = "divvy/2023/raw/"


# Connect to the public Divvy bucket
source_s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

# Connect to my AWS account
session = boto3.Session(profile_name="rami-main")
destination_s3 = session.client("s3", region_name="eu-central-1")

# January 2023 - December 2023

list_source_key = ["202301-divvy-tripdata.zip",
                   "202302-divvy-tripdata.zip",
                   "202303-divvy-tripdata.zip",
                   "202304-divvy-tripdata.zip",
                   "202305-divvy-tripdata.zip",
                   "202306-divvy-tripdata.zip",
                   "202307-divvy-tripdata.zip",
                   "202308-divvy-tripdata.zip",
                   "202309-divvy-tripdata.zip",
                   "202310-divvy-tripdata.zip",
                   "202311-divvy-tripdata.zip",
                   "202312-divvy-tripdata.zip"]

for source_key in list_source_key:
    response = source_s3.get_object(Bucket=source_bucket, Key=source_key)
    print("Successfully accessed:", source_key)
    print("File size:", response["ContentLength"], "bytes")
    # Destination path in my S3 bucket
    destination_key = destination_prefix + source_key
    # Upload the original ZIP file directly to my bucket
    destination_s3.upload_fileobj(
        response["Body"],
        destination_bucket,
        destination_key)
    print("Successfully uploaded to:")
    print(f"s3://{destination_bucket}/{destination_key}")
    # Verify that the uploaded file exists
    uploaded_file = destination_s3.head_object(
        Bucket=destination_bucket,
        Key=destination_key)
    print("Uploaded file size:", uploaded_file["ContentLength"], "bytes")