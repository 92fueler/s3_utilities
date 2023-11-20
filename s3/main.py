from s3.s3 import S3Config

# create a s3_config instance with desired configuration
s3_config = S3Config(
    region_name="us-east-1",
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key",
    use_ssl=True,
)
