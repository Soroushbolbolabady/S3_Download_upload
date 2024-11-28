import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

load_dotenv()

#sync a folder to s3

s3 = boto3.client('s3', aws_access_key_id= os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),)
def upload_files(local_directory, bucket_name, s3_prefix=''):
    try:
        # Walk through the directory
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                # Construct the full local path
                local_path = os.path.join(root, file)
                
                # Construct the full S3 path
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_prefix, relative_path).replace('\\', '/')
                
                try:
                    # Upload the file
                    s3.upload_file(local_path, bucket_name, s3_path)
                    print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")
                
                except ClientError as e:
                    print(f"Error uploading {local_path}: {e}")
        
        print("Folder upload completed successfully!")
    
    except NoCredentialsError:
        print("AWS credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")



def list_of_folders(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    folders = []
    for content in response.get('Contents', []):
        key = content['Key']
        folder = key.split('/')[0]
        if folder not in folders:
            folders.append(folder)
    return folders


def download_files(bucket_name, s3_prefix, local_directory):
    try:
        # List all objects in the S3 path
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
        
        # Walk through each object
        for content in response.get('Contents', []):
            key = content['Key']
            s3_path = key
            local_path = os.path.join(local_directory, key)
            
            # Create the local directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download the file
            s3.download_file(bucket_name, s3_path, local_path)
            print(f"Downloaded s3://{bucket_name}/{s3_path} to {local_path}")
        
        print("Folder download completed successfully!")
    
    except NoCredentialsError:
        print("AWS credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")



def main():

    bucket_name = os.getenv("S3_BUCKET_NAME")

    user_input = int(input("Enter \n.1 to upload files to s3, \n.2 to download files from s3, \n.3 to list folders in s3, \n.4 to download a folder from s3.\n "))
    if user_input == 1:
        local_directory = input("Enter the local directory: ")
        s3_prefix = input("Enter the s3 prefix: ")
        upload_files(local_directory, bucket_name, s3_prefix)
    elif user_input == 2:
        s3_prefix = input("Enter the s3 prefix: ")
        local_directory = input("Enter the local directory: ")
        download_files(bucket_name, s3_prefix, local_directory)
    elif user_input == 3:
        print(list_of_folders(bucket_name))
        main()
    elif user_input == 4:
        s3_prefix = input("Enter the s3 prefix: ")
        local_directory = input("Enter the local directory: ")
        download_files(bucket_name, s3_prefix, local_directory)
    else:
        print("Invalid input")
        main()



if __name__ == "__main__":
    main()