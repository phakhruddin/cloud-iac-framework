# AWS CDK Python Implementation

This directory contains an implementation of AWS infrastructure using AWS CDK with Python. It demonstrates how to define and deploy AWS resources using infrastructure as code.

## Project Structure

```
python/
├── README.md           # This file
├── setup.py            # Package setup file
├── requirements.txt    # Python dependencies
├── app.py              # Main CDK app entry point
└── stacks/             # CDK stack definitions
    ├── __init__.py
    ├── network_stack.py   # VPC, subnets, etc.
    ├── compute_stack.py   # EC2, Lambda, etc.
    └── database_stack.py  # RDS, DynamoDB, etc.
```

## Prerequisites

- Python 3.7 or higher
- AWS account and configured AWS CLI
- AWS CDK Toolkit

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the AWS CDK Toolkit:
   ```bash
   npm install -g aws-cdk
   ```

4. Bootstrap your AWS environment (if not already done):
   ```bash
   cdk bootstrap aws://ACCOUNT-NUMBER/REGION
   ```

## Deployment

1. Synthesize CloudFormation template:
   ```bash
   cdk synth
   ```

2. View changes before deployment:
   ```bash
   cdk diff
   ```

3. Deploy the stacks:
   ```bash
   cdk deploy --all
   ```
   
   Or deploy individual stacks:
   ```bash
   cdk deploy NetworkStack
   ```

4. Destroy the stacks when no longer needed:
   ```bash
   cdk destroy --all
   ```

## Stack Details

### Network Stack (`network_stack.py`)

The network stack creates:
- VPC with public and private subnets across multiple AZs
- Internet Gateway and NAT Gateways
- Route Tables and Network ACLs
- Security Groups with appropriate rules

Example usage:

```python
from aws_cdk import core, aws_ec2 as ec2

class NetworkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create VPC
        self.vpc = ec2.Vpc(
            self, "MainVPC",
            max_azs=2,
            cidr="10.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                )
            ]
        )
```

### Compute Stack (`compute_stack.py`)

The compute stack creates:
- EC2 instances
- Auto Scaling Groups
- Lambda Functions
- Container Services (ECS/Fargate)

### Database Stack (`database_stack.py`)

The database stack creates:
- RDS instances
- DynamoDB tables
- ElastiCache clusters

## Configuration

Environment-specific configuration is stored in `cdk.json`:

```json
{
  "app": "python app.py",
  "context": {
    "dev": {
      "vpc_cidr": "10.0.0.0/16",
      "instance_type": "t3.micro",
      "db_instance_type": "db.t3.small"
    },
    "prod": {
      "vpc_cidr": "10.1.0.0/16",
      "instance_type": "m5.large",
      "db_instance_type": "db.m5.large"
    }
  }
}
```

Access context values in your stacks:

```python
env = self.node.try_get_context("dev")
instance_type = ec2.InstanceType(env["instance_type"])
```

## Testing

This project uses pytest for testing:

```bash
pytest
```

## Best Practices

1. **Use Constructs**: Make your code reusable with L3 constructs
2. **Stack Separation**: Keep stacks focused on specific concerns
3. **Parameter Store**: Use AWS SSM Parameter Store for sensitive values
4. **Tagging**: Add tags to all resources for better management
5. **Context Values**: Use context for environment-specific configuration
