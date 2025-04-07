#!/usr/bin/env python3

import aws_cdk as cdk
from stacks.s3_bucket_stack import S3BucketStack

app = cdk.App()

S3BucketStack(app, "S3BucketStack")

app.synth()
