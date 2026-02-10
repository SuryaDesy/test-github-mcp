import pulumi
import pulumi_aws as aws
import json

# Get configuration
config = pulumi.Config()
client = config.require("client")
env = config.require("env")

# Tags to apply to all resources
tags = {
    "application": "contido",
    "product": "contido_webapp",
    "environment": env,
    "client": client,
    "iac": "pulumi",
}

# ============================================================================
# Upload Bucket Configuration
# ============================================================================
upload_bucket = aws.s3.Bucket("upload-bucket",
    bucket=f"contido-{client}-upload-{env}",
    tags=tags)

upload_encryption = aws.s3.BucketServerSideEncryptionConfiguration("upload-encryption",
    bucket=upload_bucket.id,
    rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256",
        ),
    ))

upload_cors = aws.s3.BucketCorsConfiguration("upload-cors",
    bucket=upload_bucket.id,
    cors_rules=[aws.s3.BucketCorsConfigurationCorsRuleArgs(
        allowed_headers=["*"],
        allowed_methods=["HEAD", "GET", "PUT", "POST"],
        allowed_origins=["*"],
        expose_headers=[],
    )])

upload_public_access = aws.s3.BucketPublicAccessBlock("upload-public-access",
    bucket=upload_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True)

upload_ownership = aws.s3.BucketOwnershipControls("upload-ownership",
    bucket=upload_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="BucketOwnerEnforced",
    ))

# ============================================================================
# MAM Bucket Configuration
# ============================================================================
mam_bucket = aws.s3.Bucket("mam-bucket",
    bucket=f"contido-{client}-mam-{env}",
    tags=tags)

mam_encryption = aws.s3.BucketServerSideEncryptionConfiguration("mam-encryption",
    bucket=mam_bucket.id,
    rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256",
        ),
    ))

mam_cors = aws.s3.BucketCorsConfiguration("mam-cors",
    bucket=mam_bucket.id,
    cors_rules=[aws.s3.BucketCorsConfigurationCorsRuleArgs(
        allowed_headers=["*"],
        allowed_methods=["HEAD", "GET", "PUT", "POST"],
        allowed_origins=["*"],
        expose_headers=[],
    )])

mam_public_access = aws.s3.BucketPublicAccessBlock("mam-public-access",
    bucket=mam_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True)

mam_ownership = aws.s3.BucketOwnershipControls("mam-ownership",
    bucket=mam_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="BucketOwnerEnforced",
    ))

# ============================================================================
# Asset Bucket Configuration
# ============================================================================
asset_bucket = aws.s3.Bucket("asset-bucket",
    bucket=f"contido-{client}-asset-{env}",
    tags=tags)

asset_encryption = aws.s3.BucketServerSideEncryptionConfiguration("asset-encryption",
    bucket=asset_bucket.id,
    rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256",
        ),
    ))

asset_cors = aws.s3.BucketCorsConfiguration("asset-cors",
    bucket=asset_bucket.id,
    cors_rules=[aws.s3.BucketCorsConfigurationCorsRuleArgs(
        allowed_headers=["*"],
        allowed_methods=["HEAD", "GET", "PUT", "POST"],
        allowed_origins=["*"],
        expose_headers=[],
    )])

asset_public_access = aws.s3.BucketPublicAccessBlock("asset-public-access",
    bucket=asset_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True)

asset_ownership = aws.s3.BucketOwnershipControls("asset-ownership",
    bucket=asset_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="BucketOwnerEnforced",
    ))

# ============================================================================
# Archive Bucket Configuration
# ============================================================================
archive_bucket = aws.s3.Bucket("archive-bucket",
    bucket=f"contido-{client}-archive-{env}",
    tags=tags)

archive_encryption = aws.s3.BucketServerSideEncryptionConfiguration("archive-encryption",
    bucket=archive_bucket.id,
    rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256",
        ),
    ))

archive_versioning = aws.s3.BucketVersioningV2("archive-versioning",
    bucket=archive_bucket.id,
    versioning_configuration=aws.s3.BucketVersioningV2VersioningConfigurationArgs(
        status="Enabled",
    ))

archive_public_access = aws.s3.BucketPublicAccessBlock("archive-public-access",
    bucket=archive_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True)

archive_ownership = aws.s3.BucketOwnershipControls("archive-ownership",
    bucket=archive_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="ObjectWriter",
    ))

# ============================================================================
# Edit Bucket Configuration
# ============================================================================
edit_bucket = aws.s3.Bucket("edit-bucket",
    bucket=f"contido-{client}-edit-{env}",
    tags=tags)

edit_encryption = aws.s3.BucketServerSideEncryptionConfiguration("edit-encryption",
    bucket=edit_bucket.id,
    rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256",
        ),
    ))

edit_public_access = aws.s3.BucketPublicAccessBlock("edit-public-access",
    bucket=edit_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True)

edit_ownership = aws.s3.BucketOwnershipControls("edit-ownership",
    bucket=edit_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="BucketOwnerEnforced",
    ))

# ============================================================================
# Export bucket names
# ============================================================================
pulumi.export("upload_bucket_name", upload_bucket.id)
pulumi.export("mam_bucket_name", mam_bucket.id)
pulumi.export("asset_bucket_name", asset_bucket.id)
pulumi.export("archive_bucket_name", archive_bucket.id)
pulumi.export("edit_bucket_name", edit_bucket.id)
