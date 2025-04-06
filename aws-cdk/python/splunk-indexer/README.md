# Splunk Indexer AWS CDK Implementation

This AWS CDK Python implementation creates a Splunk indexer cluster with the following architecture:

- EC2 instances in an Auto Scaling Group
- Instances placed in private subnets for security
- Network Load Balancer (NLB) for client connections
- Cross-account access configuration via AWS RAM
- Security groups with proper access rules

## Prerequisites

- [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) installed
- Python 3.7 or higher
- AWS account and credentials configured
- Splunk AMI available in your account

## Deployment

### 1. Install dependencies

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure the stack

Edit the `app.py` file to configure:

- `cross_account_ids`: List of AWS account IDs that need access to the Splunk indexers
- `splunk_ami_id`: The AMI ID of your Splunk image
- `instance_type`: EC2 instance type for your Splunk indexers
- Scaling parameters: min, max, and desired capacity

### 3. Deploy the stack

```bash
# Bootstrap CDK (if not already done)
cdk bootstrap

# Synthesize CloudFormation template
cdk synth

# Deploy the stack
cdk deploy
```

## Security Considerations

- All Splunk indexers are deployed in private subnets
- Security groups restrict traffic to only necessary ports (8089, 9997)
- IAM roles follow least privilege principle
- Traffic between accounts is secured via AWS network infrastructure

## Cross-Account Access

After deployment, you need to accept the Resource Share invitation in each target AWS account.
