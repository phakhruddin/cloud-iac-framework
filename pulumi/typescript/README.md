# Pulumi TypeScript Implementation

This directory contains a cloud-agnostic infrastructure implementation using Pulumi with TypeScript. It demonstrates how to define and deploy cloud resources across multiple providers.

## Project Structure

```
typescript/
├── README.md           # This file
├── Pulumi.yaml         # Project configuration
├── package.json        # npm dependencies and scripts
├── tsconfig.json       # TypeScript configuration
├── index.ts            # Main entry point
└── modules/            # Pulumi modules
    ├── network.ts      # Network resources
    ├── compute.ts      # Compute resources
    └── database.ts     # Database resources
```

## Prerequisites

- Node.js 14.x or higher
- Pulumi CLI
- Cloud provider accounts and credentials:
  - AWS
  - Azure
  - Google Cloud

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Login to Pulumi:
   ```bash
   pulumi login
   ```

3. Create a new stack:
   ```bash
   pulumi stack init dev
   ```

4. Configure your cloud provider(s):
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

### Network Module (`network.ts`)

This module creates networking resources:
- Virtual Networks
- Subnets
- Security Groups / Firewall Rules
- Gateways

Example usage with AWS:

```typescript
import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';

export interface NetworkArgs {
    name: string;
    cidrBlock: string;
    azCount: number;
}

export class Network extends pulumi.ComponentResource {
    public vpc