# Contido Infrastructure - Pulumi (Python)

Complete Pulumi Infrastructure as Code for the Contido application, converted from Terraform.

## Overview

This Pulumi project spans the complete AWS infrastructure for Contido, including:

### Compute & Networking
- **Lambda Functions**: Sync service and file ingest service
- **Event Source Mappings**: Triggered by SQS queues

### Storage
- **S3 Buckets**: Upload, MAM, Asset, Archive, and Edit buckets
- **Bucket Configurations**: Encryption, CORS, public access blocks, versioning

### Content Delivery
- **CloudFront Distributions**: Proxy, Thumbnail, and Asset CDNs
- **Origin Access Identities (OAI)**: Secure S3 access from CloudFront
- **Route53 Records**: DNS aliases for CDN domains (optional)

### Access & Security
- **IAM Policies**: Resource access, secret manager, Lambda basic permissions, CDN invalidation
- **IAM Roles**: Lambda execution role with attached policies
- **IAM Users**: Backend, Frontend, and Aspera users with specific permissions

### Messaging
- **SQS Queues**: 
  - Upload event notifications
  - MAM bucket restore and storage
  - File transfer and ingest
  - Transcoding workflows
  - Client delivery
  - Archive watch folder
  - Lambda service queues
- **Queue Policies**: S3 bucket to queue permissions

## Prerequisites

1. **Pulumi CLI**: [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
2. **Python 3.7+**: [Install Python](https://www.python.org/)
3. **AWS CLI**: [Install AWS CLI](https://aws.amazon.com/cli/) and configure credentials
4. **AWS Account**: Valid AWS credentials configured with appropriate permissions

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

### 5. Configure Your Stack

Create or select a stack:

```bash
pulumi stack select dev  # or create: pulumi stack init dev
```

Set required configuration values:

```bash
pulumi config set client "acme"
pulumi config set env "development"
pulumi config set aws:region "ap-south-1"
pulumi config set account_id "909463554763"
```

Set optional CloudFront/Route53 configuration:

```bash
pulumi config set cache_policy_id "your-policy-id"
pulumi config set origin_request_policy_id "your-policy-id"
pulumi config set acm_certificate_arn "arn:aws:acm:..."
pulumi config set r53_zone_id "your-zone-id"
```

Set Lambda Docker image URIs (if deploying Lambda functions):

```bash
pulumi config set image_uri_sync "your-account.dkr.ecr.ap-south-1.amazonaws.com/sync-service:latest"
pulumi config set image_uri_ingest "your-account.dkr.ecr.ap-south-1.amazonaws.com/ingest-service:latest"
```

## Usage

### Preview Changes

```bash
pulumi preview
```

### Deploy Infrastructure

```bash
pulumi up
```

This will show a preview of resources to be created. Review and confirm with `yes`.

### View Stack Outputs

```bash
pulumi stack output
pulumi stack output upload_bucket_name
```

### Destroy Infrastructure

```bash
pulumi destroy
```

## Project Structure

```
.
├── Pulumi.yaml                 # Pulumi project metadata
├── __main__.py                 # Complete Pulumi program (all resources)
├── Pulumi.dev.yaml            # Development stack config
├── Pulumi.prod.yaml           # Production stack config
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore patterns
└── README.md                  # This file
```

## Configuration Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `client` | string | Yes | - | Client name (used in resource naming) |
| `env` | string | Yes | - | Environment (dev, staging, prod) |
| `aws:region` | string | Yes | - | AWS region |
| `account_id` | string | Yes | - | AWS account ID (for IAM ARNs) |
| `cache_policy_id` | string | No | CloudFront default | CloudFront cache policy |
| `origin_request_policy_id` | string | No | CloudFront default | Origin request policy |
| `response_headers_policy_id` | string | No | Empty | Response headers policy |
| `acm_certificate_arn` | string | No | Uses CloudFront cert | ACM certificate ARN |
| `r53_zone_id` | string | No | Optional | Route53 hosted zone ID |
| `image_uri_sync` | string | No | Placeholder | Docker image URI for sync Lambda |
| `image_uri_ingest` | string | No | Placeholder | Docker image URI for ingest Lambda |
| `memory_size` | number | No | 1024 | Lambda memory allocation (MB) |
| `ephemeral_storage_size` | number | No | 2048 | Lambda ephemeral storage (MB) |
| `batch_size` | number | No | 1 | SQS batch size for Lambda |

## Resources Created

### S3 Buckets (per stack)
| Bucket | Purpose | Features |
|--------|---------|----------|
| Upload | File uploads with S3 notifications | Event notifications to SQS |
| MAM | Media asset management | Versioning, multi-queue notifications |
| Asset | Static assets serving | CloudFront origin |
| Archive | Long-term storage | Versioning enabled, archive notifications |
| Edit | Edit workflow storage | Standard configuration |

### Lambda Functions
- **Sync Service**: Triggered by sync-service SQS queue
- **File Ingest Service**: Triggered by file-ingest-service SQS queue

### SQS Queues (per stack - 9 total)
1. Upload event notifications
2. MAM restore folder
3. File transfer
4. Ingest proxy
5. Transcoding start
6. Client delivery
7. Archive watch folder
8. Sync service
9. File ingest service

### IAM Resources
- **3 Users**: Backend, Frontend, Aspera
- **1 Role**: Lambda execution role
- **6 Policies**: Resource access, secret manager, Lambda logs, FE asset access, CDN invalidation, Aspera upload

### CloudFront & DNS
- **3 CDN Distributions**: Proxy, Thumbnail, Asset
- **3 Origin Access Identities**: Secure S3 access
- **3 Route53 Records** (optional): DNS aliases

## Differences from Terraform

### Benefits of Pulumi
- ✅ Full programming language (Python) for complex logic
- ✅ Type safety with IDE support
- ✅ Better code organization and reusability
- ✅ Cleaner syntax for complex resources
- ✅ Native support for conditional resources

### Key Implementation Notes
1. **CloudFront Defaults**: If ACM certificate not provided, uses CloudFront default certificate
2. **Lambda Optionality**: Lambda functions only created if image URIs are provided
3. **Route53 Records**: Only created if `r53_zone_id` is configured
4. **Conditional Policies**: Response headers policy is optional
5. **SQS Policies**: Automatically configured with least-privilege S3 source restrictions

## IAM Policy Details

### Resources Access Policy
- S3: List, Get, Put, Delete on all buckets
- SQS: Send, Receive, Delete, Get attributes

### Secret Manager Policy
- SecretsManager: GetSecretValue
- KMS: Decrypt

### Lambda Policy
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

### FE Asset Policy
- S3 asset bucket: List and object operations

### CDN Invalidation Policy
- CloudFront: CreateInvalidation

### Aspera Policy
- S3 upload bucket: List and object operations

## Outputs

The stack exports the following values:

```bash
pulumi stack output [output_name]
```

**Available outputs:**
- Bucket names (all 5 buckets)
- Queue URLs (all 9 queues)
- Lambda function names (if configured)
- CloudFront domain names (all 3 distributions)
- Route53 record names (if configured)
- IAM resource names (users, role, policies)

## Security Best Practices

✅ **Implemented in this configuration:**
- Server-side encryption on all S3 buckets
- Block public access on all buckets
- CloudFront OAIs for secure S3 access
- Bucket policies with least-privilege access
- IAM policies with specific resource restrictions
- SQS managed encryption enabled
- VPC security groups (if Lambda in VPC)
- Least-privilege IAM principles throughout

## Deployment Examples

### Development Environment

```bash
pulumi stack select dev
pulumi config set client "test-client"
pulumi config set env "dev"
pulumi up
```

### Production Environment with Full Configuration

```bash
pulumi stack select prod
pulumi config set client "acme-corp"
pulumi config set env "prod"
pulumi config set acm_certificate_arn "arn:aws:acm:..."
pulumi config set r53_zone_id "Z1234567890ABC"
pulumi config set image_uri_sync "112345678901.dkr.ecr.ap-south-1.amazonaws.com/sync:v1.0"
pulumi config set image_uri_ingest "112345678901.dkr.ecr.ap-south-1.amazonaws.com/ingest:v1.0"
pulumi up
```

## Troubleshooting

### 1. CloudFront Distribution Creation Fails
**Issue**: S3 bucket policies have circular dependencies
**Solution**: Bucket policies automatically depend on distributions in this code

### 2. Lambda Function Fails to Deploy
**Issue**: Docker image URI not accessible
**Solution**: Ensure `image_uri_sync` and `image_uri_ingest` are valid and in ECR

### 3. Route53 Records Not Created
**Issue**: `r53_zone_id` is required
**Solution**: Either provide the zone ID or manually create Route53 records

### 4. SQS to S3 Notifications Not Working
**Issue**: Missing queue policies
**Solution**: Policies are automatically created with proper S3 source restrictions

## Next Steps

1. **Add VPC & Security Groups** for Lambda functions
2. **Implement Auto-Scaling** for Lambda concurrency
3. **Add CloudWatch Monitoring** and alarms
4. **Setup CI/CD Pipeline** with Pulumi automation API
5. **Add Data Lifecycle Policies** for S3 buckets
6. **Implement Multi-Region Disaster Recovery**
7. **Add Cost Allocation Tags** for billing analysis

## Conversion from Terraform

This Pulumi project replaces the original Terraform configuration files:
- `s3.tf` → S3 buckets section
- `cdn.tf` → CloudFront and Route53 sections
- `iam_policies.tf` → IAM policies section
- `iam-role.tf` → IAM roles section
- `iam-user.tf` → IAM users section
- `lambda.tf` → Lambda functions section
- `sqs.tf` → SQS queues section
- `r53.tf` → Route53 records section
- `var.tf` → Pulumi configuration
- `providers.tf` → AWS provider setup

## Support

- **Pulumi Docs**: https://www.pulumi.com/docs/
- **Pulumi AWS Provider**: https://www.pulumi.com/registry/packages/aws/
- **GitHub Issues**: Report issues in the repository

## License

[Add your license information here]

---

**Last Updated**: 2026-02-10
**Pulumi Version**: >= 3.0.0
**Python Version**: >= 3.7
