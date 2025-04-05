# Pulumi Python Implementation

This directory contains a cloud-agnostic infrastructure implementation using Pulumi with Python. It demonstrates how to define and deploy cloud resources across multiple providers.

## Project Structure

```
python/
├── README.md           # This file
├── Pulumi.yaml         # Project configuration
├── requirements.txt    # Python dependencies
├── __main__.py         # Main entry point
└── modules/            # Pulumi modules
    ├── __init__.py
    ├── network.py      # Network resources
    ├── compute.py      # Compute resources
    └── database.py     # Database resources
```

## Prerequisites

- Python 3.7 or higher
- Pulumi CLI
- Cloud provider accounts and credentials:
  - AWS
  - Azure
  - Google Cloud

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

3. Login to Pulumi:
   ```bash
   pulumi login
   ```

4. Create a new stack:
   ```bash
   pulumi stack init dev
   ```

5. Configure your cloud provider(s):
   ```bash
   # For AWS
   pulumi config set aws:region us-west-2
   # For Azure
   pulumi config set azure:location westus2
   # For GCP
   pulumi config set gcp:project my-project
   pulumi config set gcp:zone us-central1-a
   ```

## Deployment

1. Preview changes:
   ```bash
   pulumi preview
   ```

2. Deploy resources:
   ```bash
   pulumi up
   ```

3. Destroy resources when no longer needed:
   ```bash
   pulumi destroy
   ```

## Module Details

### Network Module (`network.py`)

This module creates networking resources:
- Virtual Networks
- Subnets
- Security Groups / Firewall Rules
- Gateways

Example usage with AWS:

```python
import pulumi
import pulumi_aws as aws

def create_network(name, cidr="10.0.0.0/16", azs=2):
    # Create a VPC
    vpc = aws.ec2.Vpc(f"{name}-vpc",
        cidr_block=cidr,
        enable_dns_hostnames=True,
        enable_dns_support=True,
        tags={"Name": f"{name}-vpc"}
    )

    # Create public and private subnets
    public_subnets = []
    private_subnets = []
    
    for i in range(azs):
        public_subnet = aws.ec2.Subnet(f"{name}-public-{i}",
            vpc_id=vpc.id,
            cidr_block=f"10.0.{i}.0/24",
            availability_zone=aws.get_availability_zones().names[i],
            map_public_ip_on_launch=True,
            tags={"Name": f"{name}-public-{i}"}
        )
        public_subnets.append(public_subnet)
        
        private_subnet = aws.ec2.Subnet(f"{name}-private-{i}",
            vpc_id=vpc.id,
            cidr_block=f"10.0.{i+100}.0/24",
            availability_zone=aws.get_availability_zones().names[i],
            tags={"Name": f"{name}-private-{i}"}
        )
        private_subnets.append(private_subnet)
    
    return {
        "vpc": vpc,
        "public_subnets": public_subnets,
        "private_subnets": private_subnets
    }
```

Example usage with Azure:

```python
import pulumi
import pulumi_azure_native as azure_native

def create_network(name, cidr="10.0.0.0/16"):
    # Create a resource group
    resource_group = azure_native.resources.ResourceGroup(f"{name}-rg")
    
    # Create a virtual network
    vnet = azure_native.network.VirtualNetwork(f"{name}-vnet",
        resource_group_name=resource_group.name,
        address_space=azure_native.network.AddressSpaceArgs(
            address_prefixes=[cidr],
        ),
        location=resource_group.location,
    )
    
    # Create subnets
    subnet = azure_native.network.Subnet(f"{name}-subnet",
        resource_group_name=resource_group.name,
        virtual_network_name=vnet.name,
        address_prefix="10.0.0.0/24",
    )
    
    return {
        "resource_group": resource_group,
        "vnet": vnet,
        "subnet": subnet
    }
```

### Compute Module (`compute.py`)

This module creates compute resources:
- Virtual Machines / Instances
- Serverless Functions
- Container Resources

### Database Module (`database.py`)

This module creates database resources:
- Managed SQL Databases
- NoSQL Databases
- Caching Services

## Multi-Cloud Configuration

The Pulumi stack configuration (`Pulumi.<stack-name>.yaml`) can specify which cloud provider to use:

```yaml
config:
  cloud-provider: aws  # can be 'aws', 'azure', or 'gcp'
  aws:region: us-west-2
  azure:location: westus2
  gcp:project: my-project
  gcp:zone: us-central1-a
```

In your code, you can check the provider and use the appropriate resources:

```python
import pulumi

config = pulumi.Config()
provider = config.get("cloud-provider") or "aws"

if provider == "aws":
    # Use AWS resources
    import modules.aws as cloud
elif provider == "azure":
    # Use Azure resources
    import modules.azure as cloud
elif provider == "gcp":
    # Use GCP resources
    import modules.gcp as cloud
```

## Testing

This project uses Pulumi's testing framework:

```bash
python -m unittest discover tests
```

## Best Practices

1. **Abstraction**: Create provider-agnostic interfaces where possible
2. **Component Resources**: Build reusable components
3. **Configuration**: Use Pulumi Config for environment variables
4. **Secret Management**: Use Pulumi's secret management for sensitive data
5. **Tagging**: Apply consistent tagging across all resources
6. **Stack References**: Share outputs between stacks
7. **State Management**: Use Pulumi's state management for reliable deployments
