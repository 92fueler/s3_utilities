from dataclasses import asdict, dataclass
import os
from typing import Optional

import boto3


@dataclass
class S3Config:
    region_name: str = os.getenv("AWS_REGION", "us-west-2")
    endpoint_url: Optional[str] = os.getenv("S3_ENDPOINT_URL", None)
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID", None)
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY", None)
    use_ssl: bool = True

    def __post_init__(self):
        if self.endpoint_url:
            self.use_ssl = self.endpoint_url.startswith("https://")


class S3:
    def __init__(self, s3_config: S3Config):
        self.s3_config = s3_config
        self.s3_client = self._create_s3_client()

    def _create_s3_client(self):
        try:
            return boto3.client("s3", **asdict(self.s3_config))
        except Exception as e:
            print(f"Error creating S3 client: {e}")
            raise

    def retrieve_object(self, bucket_name: str, object_key: str) -> str:
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            object_content = response["Body"].read()
            return object_content.decode("utf-8")
        except Exception as e:
            print(f"Error retrieving object with key {object_key}: {e}")
            return ""

    def retrieve_objects(self, bucket_name: str) -> None:
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if "Contents" in response:
                for obj in response["Contents"]:
                    object_key = obj["Key"]
                    object_content = self.retrieve_object(bucket_name, object_key)
                    print(f"Retrieved object with key: {object_key}")
                    print(f"Object content: {object_content}")
            else:
                print(f"No objects found in the bucket {bucket_name}")
        except Exception as e:
            print(f"Error retrieving objects in bucket {bucket_name}: {e}")

    def retrieve_paginated_objects(self, bucket_name: str, prefix: str) -> None:
        try:
            paginator = self.s3_client.get_paginator("list_objects_v2")
            list_objects_params = {"Bucket": bucket_name, "Prefix": prefix}

            for page in paginator.paginate(**list_objects_params):
                if "Contents" in page:
                    for obj in page["Contents"]:
                        object_key = obj["Key"]
                        print(f"Object Key: {object_key}")
        except Exception as e:
            print(f"Error retrieving paginated objects in bucket {bucket_name}: {e}")
