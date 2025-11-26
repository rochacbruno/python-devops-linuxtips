from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider, AwsProviderEndpoints
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket


class AwsInfraStack(TerraformStack):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        # Provider AWS
        AwsProvider(
            self,
            "aws",
            region="us-east-1",
            endpoints=[
                AwsProviderEndpoints(
                    ec2="http://localhost:4566",
                    iam="http://localhost:4566",
                    sts="http://localhost:4566",
                    s3="http://s3.localhost.localstack.cloud:4566",
                ),
            ],
            access_key="test",
            secret_key="test",
            skip_credentials_validation=True,
            skip_metadata_api_check="true",
            skip_requesting_account_id=True,
            s3_use_path_style=True,  # Critical for LocalStack S3
        )
        # Bucket S3
        bucket = S3Bucket(
            self,
            "my-bucket",
            bucket="my-cdktf-bucket-demo-123",
            tags={"Environment": "Dev"},
            timeouts={"create": "1m", "update": "1m", "delete": "1m"},
        )

        # EC2 Instance
        instance = Instance(
            self,
            "web-server",
            ami="ami-ff0fea8310f3",
            instance_type="m5.large",  # Use non-burstable instance (no credit_specification)
            tags={"Name": "WebServer"},
            # Add timeouts to prevent hanging
            timeouts={"create": "2m", "update": "2m", "delete": "2m"},
        )

        # Outputs
        TerraformOutput(self, "bucket_name", value=bucket.bucket)
        TerraformOutput(self, "instance_ip", value=instance.public_ip)


app = App()
AwsInfraStack(app, "aws-infra")
app.synth()
