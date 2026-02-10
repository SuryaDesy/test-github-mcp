# Contido Infrastructure - Pulumi (Python)

This repository contains the Pulumi Infrastructure as Code (IaC) for the Contido application, converted from Terraform.

## Overview

This Pulumi project manages AWS S3 buckets and their configurations for the Contido infrastructure, including:

- **Upload Bucket**: For file uploads
- **MAM Bucket**: For Media Asset Management with restore and storage notifications
- **Asset Bucket**: For asset storage
- **Archive Bucket**: For archival with versioning enabled
- **Edit Bucket**: For editing workflows

## Prerequisites

1. **Pulumi CLI**: [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
2. **Python 3.7+**: [Install Python](https://www.python.org/)
3. **AWS CLI**: [Install AWS CLI](https://aws.amazon.com/cli/) and configure credentials
4. **AWS Account**: Valid AWS credentials configured

## Setup

### 1. Install Pulumi

```bash
curl -fsSL https://get.pulumi.com | sh
```

### 2. Clone the Repository

```bash
git clone https://github.com/SuryaDesy/test-github-mcp.git
cd test-github-mcp
```

### 3. Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Configuration

Create a `Pulumi.<stack>.yaml` file with your stack configuration:

```bash
pulumi stack select dev  # or create: pulumi stack init dev
pulumi config set client "my-client"
pulumi config set env "dev"
pulumi config set aws:region "us-east-1"
```

## Usage

### Deploy Infrastructure

```bash
pulumi up
```

This will show a preview of the resources to be created. Review and confirm with `yes`.

### Destroy Infrastructure

```bash
pulumi destroy
```

### View Stack Outputs

```bash
pulumi stack output
```

## Project Structure

```
.
├── Pulumi.yaml          # Pulumi project metadata
├── __main__.py          # Main Pulumi program
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Configuration Parameters

| Parameter | Type   | Description |
|-----------|--------|-------------|
| `client`  | string | Client name (used in bucket naming) |
| `env`     | string | Environment name (dev, staging, prod) |
| `aws:region` | string | AWS region for resources |

## Resources Created

### S3 Buckets
- Upload bucket with CORS and event notifications
- MAM bucket with multi-queue notifications for restore and storage
- Asset bucket with standard configuration
- Archive bucket with versioning enabled
- Edit bucket for editing workflows

### Security Features
- Server-side encryption (AES256) on all buckets
- Public access blocks on all buckets
- Bucket ownership controls
- CORS configuration for cross-origin requests

## Notes

- Bucket notifications for SQS queues are commented out in this initial version
  - These will need to be added once SQS queue references are available
- All buckets follow AWS security best practices
- Tags are applied consistently across all resources

## Converting from Terraform

This Pulumi project replaces the original Terraform configuration (`s3.tf`). 

**Key differences:**
- Terraform uses HCL syntax → Pulumi uses Python
- Terraform state is managed separately → Pulumi manages state via the Pulumi service or self-hosted backend
- Terraform modules → Pulumi classes and functions

## Next Steps

1. Add SQS queue notifications (currently commented out)
2. Add Lambda functions configuration
3. Add CloudFront distribution for asset serving
4. Implement automation for multi-environment deployments

## Support

For issues or questions about Pulumi, visit: [Pulumi Documentation](https://www.pulumi.com/docs/)
