from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3
)
from constructs import Construct

class S3BucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(
            self,
            "MySimpleBucket",
            versioned=True,
            public_read_access=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
