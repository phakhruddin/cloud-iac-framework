# Cloud Infrastructure as Code (IaC) Framework

This repository provides a comprehensive framework for implementing Infrastructure as Code (IaC) using both vendor-specific and cloud-agnostic approaches. It includes implementations for AWS CDK and Pulumi, each with support for both Python and TypeScript.

## Repository Structure

```
cloud-iac-framework/
├── aws-cdk/                    # AWS CDK implementation
│   ├── python/                 # Python implementation for AWS CDK
│   └── typescript/             # TypeScript implementation for AWS CDK
└── pulumi/                     # Pulumi implementation
    ├── python/                 # Python implementation for Pulumi
    └── typescript/             # TypeScript implementation for Pulumi
```

## Implementations

### AWS CDK (Vendor-Specific)

The AWS Cloud Development Kit (CDK) is an open-source software development framework to define cloud infrastructure in code and provision it through AWS CloudFormation. This repository provides implementations in:

- [Python](./aws-cdk/python/README.md)
- [TypeScript](./aws-cdk/typescript/README.md)

### Pulumi (Cloud-Agnostic)

Pulumi is an open-source infrastructure as code tool that allows you to create, deploy, and manage infrastructure on any cloud using familiar programming languages. This repository provides implementations in:

- [Python](./pulumi/python/README.md)
- [TypeScript](./pulumi/typescript/README.md)

## Getting Started

Please refer to the README.md files in each implementation directory for specific setup and usage instructions.

## Common Infrastructure Components

Each implementation provides infrastructure code for common cloud components:

- Network (VPC, Subnets, Security Groups)
- Compute (EC2, Lambda, Container services)
- Database (RDS, DynamoDB, etc.)

## Best Practices

- **Modularity**: Each implementation follows modular design principles
- **Environment Separation**: Support for different environments (dev, staging, prod)
- **Parameterization**: Using configuration files for environment-specific values
- **Testing**: Infrastructure testing where applicable
- **CI/CD Integration**: Example CI/CD integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
