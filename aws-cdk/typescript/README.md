# AWS CDK TypeScript Implementation

This directory contains an implementation of AWS infrastructure using AWS CDK with TypeScript. It demonstrates how to define and deploy AWS resources using infrastructure as code.

## Project Structure

```
typescript/
├── README.md           # This file
├── package.json        # npm dependencies and scripts
├── tsconfig.json       # TypeScript configuration
├── bin/
│   └── app.ts          # CDK app entry point
├── lib/
│   ├── network-stack.ts    # VPC, subnets, etc.
│   ├── compute-stack.ts    # EC2, Lambda, etc.
│   └── database-stack.ts   # RDS, DynamoDB, etc.
└── test/               # Unit tests
    └── app.test.ts     # Tests for the CDK stacks
```

## Prerequisites

- Node.js 14.x or higher
- AWS account and configured AWS CLI
- AWS CDK Toolkit

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Install the AWS CDK Toolkit:
   ```bash
   npm install -g aws-cdk
   ```

3. Bootstrap your AWS environment (if not already done):
   ```bash
   cdk bootstrap aws://ACCOUNT-NUMBER/REGION
   ```

## Deployment

1. Compile TypeScript to JavaScript:
   ```bash
   npm run build
   ```

2. Synthesize CloudFormation template:
   ```bash
   cdk synth
   ```

3. View changes before deployment:
   ```bash
   cdk diff
   ```

4. Deploy the stacks:
   ```bash
   cdk deploy --all
   ```
   
   Or deploy individual stacks:
   ```bash
   cdk deploy NetworkStack
   ```

5. Destroy the stacks when no longer needed:
   ```bash
   cdk destroy --all
   ```

## Stack Details

### Network Stack (`network-stack.ts`)

The network stack creates:
- VPC with public and private subnets across multiple AZs
- Internet Gateway and NAT Gateways
- Route Tables and Network ACLs
- Security Groups with appropriate rules

Example usage:

```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class NetworkStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create VPC
    this.vpc = new ec2.Vpc(this, 'MainVPC', {
      maxAzs: 2,
      cidr: '10.0.0.0/16',
      subnetConfiguration: [
        {
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrMask: 24,
        },
      ],
    });
  }
}
```

### Compute Stack (`compute-stack.ts`)

The compute stack creates:
- EC2 instances
- Auto Scaling Groups
- Lambda Functions
- Container Services (ECS/Fargate)

### Database Stack (`database-stack.ts`)

The database stack creates:
- RDS instances
- DynamoDB tables
- ElastiCache clusters

## Configuration

Environment-specific configuration is stored in `cdk.json`:

```json
{
  "app": "npx ts-node bin/app.ts",
  "context": {
    "dev": {
      "vpcCidr": "10.0.0.0/16",
      "instanceType": "t3.micro",
      "dbInstanceType": "db.t3.small"
    },
    "prod": {
      "vpcCidr": "10.1.0.0/16",
      "instanceType": "m5.large",
      "dbInstanceType": "db.m5.large"
    }
  }
}
```

Access context values in your stacks:

```typescript
const env = this.node.tryGetContext('dev');
const instanceType = new ec2.InstanceType(env.instanceType);
```

## Testing

This project uses Jest for testing:

```bash
npm test
```

Example test:

```typescript
import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import * as NetworkStack from '../lib/network-stack';

test('VPC Created', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new NetworkStack.NetworkStack(app, 'MyTestStack');
  // THEN
  const template = Template.fromStack(stack);

  template.hasResourceProperties('AWS::EC2::VPC', {
    CidrBlock: '10.0.0.0/16',
  });
});
```

## Best Practices

1. **Constructs**: Create reusable components with L3 constructs
2. **Strong Typing**: Leverage TypeScript's type system for safer code
3. **Interfaces**: Define clear interfaces between stacks
4. **Dependency Injection**: Pass resources between stacks when needed
5. **Context Values**: Use context for environment-specific configuration
6. **Tags**: Apply consistent tagging across all resources
7. **Secrets Management**: Use AWS Secrets Manager for sensitive values
