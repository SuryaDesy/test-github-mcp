import pulumi
import pulumi_aws as aws
import json

# Get configuration
config = pulumi.Config()
client = config.require("client")
env = config.require("env")
region = config.require("aws:region")

# AWS Account ID (for ARN construction)
account_id = config.require("account_id")

# Optional variables with defaults
cache_policy_id = config.get("cache_policy_id") or ""
origin_request_policy_id = config.get("origin_request_policy_id") or ""
response_headers_policy_id = config.get("response_headers_policy_id") or ""
acm_certificate_arn = config.get("acm_certificate_arn") or ""
r53_zone_id = config.get("r53_zone_id") or ""
image_uri_sync = config.get("image_uri_sync") or ""
image_uri_ingest = config.get("image_uri_ingest") or ""
memory_size = config.get_int("memory_size") or 1024
ephemeral_storage_size = config.get_int("ephemeral_storage_size") or 2048
batch_size = config.get_int("batch_size") or 1
rule = config.get("rule") or ""
serviceaccount = config.get("serviceaccount") or ""

# Tags to apply to all resources
tags = {
    "application": "contido",
    "product": "contido_webapp",
    "environment": env,
    "client": client,
    "iac": "pulumi",
}

# Local variables for origin IDs
s3_mam_proxy_origin_id = "myS3-mam-proxy-Origin"
s3_mam_thumbnail_origin_id = "myS3-mam-thumbnail-Origin"
s3_asset_origin_id = "myS3-asset-Origin"

# ============================================================================
# S3 BUCKETS CONFIGURATION
# ============================================================================

# Upload Bucket
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

# MAM Bucket
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

# Asset Bucket
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

# Archive Bucket
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

# Edit Bucket
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
# IAM POLICIES
# ============================================================================

# Resources Access Policy
resources_access_policy = aws.iam.Policy("resources-access",
    name=f"contido-{client}-{env}-resources-access",
    description="Contido resources access policy",
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Sid":"1","Effect":"Allow","Action":["s3:ListBucket"],"Resource":[',
        pulumi.Output.concat('"', upload_bucket.arn, '","', mam_bucket.arn, '","', asset_bucket.arn, '","', archive_bucket.arn, '","', edit_bucket.arn, '"'),
        ']},',
        '{"Sid":"2","Effect":"Allow","Action":["s3:GetObject","s3:PutObject","s3:DeleteObject","s3:PutObjectAcl"],"Resource":[',
        pulumi.Output.concat('"', upload_bucket.arn, '/*","', mam_bucket.arn, '/*","', asset_bucket.arn, '/*","', archive_bucket.arn, '/*","', edit_bucket.arn, '/*"'),
        ']},',
        '{"Sid":"3","Effect":"Allow","Action":["sqs:SendMessage","sqs:ReceiveMessage","sqs:DeleteMessage","sqs:GetQueueAttributes","sqs:SetQueueAttributes"],"Resource":["*"]}',
        ']}'
    ),
    tags=tags)

# Secret Manager Access Policy
secret_manager_policy = aws.iam.Policy("secret-manager-access",
    name=f"contido-{client}-secret_manager_access",
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Effect":"Allow","Action":["secretsmanager:GetSecretValue"],"Resource":"*"},',
        '{"Effect":"Allow","Action":["kms:Decrypt"],"Resource":"*"}',
        ']}'
    ),
    tags=tags)

# Lambda Basic Permissions Policy
lambda_basic_policy = aws.iam.Policy("lambda-basic-permissions",
    name=f"lambda-{client}-basic-permissions",
    description="Lambda basic permissions policy",
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        f'{{"Effect":"Allow","Action":"logs:CreateLogGroup","Resource":"arn:aws:logs:{region}:{account_id}:*"}},',
        f'{{"Effect":"Allow","Action":["logs:CreateLogStream","logs:PutLogEvents"],"Resource":["arn:aws:logs:{region}:{account_id}:log-group:/aws/lambda/contido-{client}-{env}-*"]}}',
        ']}'
    ),
    tags=tags)

# FE Asset Bucket Access Policy
userfe_policy = aws.iam.Policy("fe-asset-bucket-access",
    name=f"contido-{client}-{env}-asset-bucket-access",
    description="FE asset bucket access policy",
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Sid":"VisualEditor0","Effect":"Allow","Action":["s3:ListBucket"],"Resource":["',
        asset_bucket.arn,
        '"]},',
        '{"Sid":"VisualEditor1","Effect":"Allow","Action":["s3:GetObject","s3:PutObject","s3:DeleteObject","s3:PutObjectAcl"],"Resource":["',
        asset_bucket.arn,
        '/*"]}',
        ']}'
    ),
    tags=tags)

# Asset CDN Invalidation Policy
cdn_invalidation_policy = aws.iam.Policy("asset-cdn-invalidation",
    name=f"Invalidate-{client}-asset_cdn_policy",
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Sid":"VisualEditor0","Effect":"Allow","Action":["cloudfront:CreateInvalidation"],"Resource":"*"}',
        ']}'
    ),
    tags=tags)

# Aspera Upload Bucket Access Policy
useraspera_policy = aws.iam.Policy("aspera-upload-access",
    name=f"contido-{client}-upload-{env}-bucket-access",
    description="Aspera upload bucket access policy",
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Effect":"Allow","Action":["s3:ListBucket"],"Resource":"arn:aws:s3:::contido-',
        client,
        '-upload-',
        env,
        '"},',
        '{"Effect":"Allow","Action":["s3:GetObject","s3:PutObject","s3:DeleteObject"],"Resource":"arn:aws:s3:::contido-',
        client,
        '-upload-',
        env,
        '/*"}',
        ']}'
    ),
    tags=tags)

# ============================================================================
# IAM ROLE
# ============================================================================

assume_role_policy = pulumi.Output.concat(
    '{"Version":"2012-10-17","Statement":[',
    '{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}',
    ']}'
)

iam_role = aws.iam.Role("backend-common-role",
    name=f"contido-{client}-{env}-backend-common-role",
    assume_role_policy=assume_role_policy,
    tags=tags)

# Attach policies to role
resources_attachment = aws.iam.RolePolicyAttachment("resources-access",
    role=iam_role.name,
    policy_arn=resources_access_policy.arn)

secret_attachment = aws.iam.RolePolicyAttachment("secret-manager-access",
    role=iam_role.name,
    policy_arn=secret_manager_policy.arn)

lambda_attachment = aws.iam.RolePolicyAttachment("lambda-basic-permissions",
    role=iam_role.name,
    policy_arn=lambda_basic_policy.arn)

# ============================================================================
# IAM USERS
# ============================================================================

# Backend User
iam_userbe = aws.iam.User("backend-user",
    name=f"contido-{client}-{env}-user",
    tags=tags)

userbe_policy_attachment = aws.iam.UserPolicyAttachment("userbe-resources-access",
    user=iam_userbe.name,
    policy_arn=resources_access_policy.arn)

# Frontend User
iam_userfe = aws.iam.User("frontend-user",
    name=f"contido-{client}-{env}-fe",
    tags=tags)

userfe_policy_attachment = aws.iam.UserPolicyAttachment("userfe-asset-access",
    user=iam_userfe.name,
    policy_arn=userfe_policy.arn)

userfe_cdn_attachment = aws.iam.UserPolicyAttachment("userfe-cdn-invalidation",
    user=iam_userfe.name,
    policy_arn=cdn_invalidation_policy.arn)

# Aspera User
iam_aspera = aws.iam.User("aspera-user",
    name=f"{client}-{env}-aspera",
    tags=tags)

useraspera_policy_attachment = aws.iam.UserPolicyAttachment("useraspera-upload-access",
    user=iam_aspera.name,
    policy_arn=useraspera_policy.arn)

# ============================================================================
# SQS QUEUES
# ============================================================================

# Upload Queue
upload_queue = aws.sqs.Queue("upload-queue",
    name=f"contido-{client}-upload-{env}",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

upload_queue_policy = aws.sqs.QueuePolicy("upload-queue-policy",
    queue_url=upload_queue.url,
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Effect":"Allow","Principal":"*","Action":["sqs:SendMessage"],"Resource":"',
        upload_queue.arn,
        '","Condition":{"ArnEquals":{"aws:SourceArn":"',
        upload_bucket.arn,
        '"}}}',
        ']}'
    ))

# MAM Restore Queue
mam_restore_queue = aws.sqs.Queue("mam-restore-queue",
    name=f"contido-{client}-restore-{env}",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

mam_restore_queue_policy = aws.sqs.QueuePolicy("mam-restore-queue-policy",
    queue_url=mam_restore_queue.url,
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Effect":"Allow","Principal":"*","Action":["sqs:SendMessage"],"Resource":"',
        mam_restore_queue.arn,
        '","Condition":{"ArnEquals":{"aws:SourceArn":"',
        mam_bucket.arn,
        '"}}}',
        ']}'
    ))

# Transfer Queue
transfer_queue = aws.sqs.Queue("transfer-queue",
    name=f"contido-{client}-transfer-{env}",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

# Ingest Proxy Queue
ingest_proxy_queue = aws.sqs.Queue("ingest-proxy-queue",
    name=f"contido-{client}-ingest-{env}-proxy",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

# Transcoding Start Queue
transcoding_start_queue = aws.sqs.Queue("transcoding-start-queue",
    name=f"contido-{client}-transcoding-start-{env}",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

# Client Delivery Queue
client_delivery_queue = aws.sqs.Queue("client-delivery-queue",
    name=f"client_delivery_{client}_{env}_sgp",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

client_delivery_policy = aws.sqs.QueuePolicy("client-delivery-queue-policy",
    queue_url=client_delivery_queue.url,
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Effect":"Allow","Principal":"*","Action":["sqs:SendMessage"],"Resource":"',
        client_delivery_queue.arn,
        '","Condition":{"ArnEquals":{"aws:SourceArn":"',
        archive_bucket.arn,
        '"}}}',
        ']}'
    ))

# Archive Queue
archive_queue = aws.sqs.Queue("archive-queue",
    name=f"contido-{client}-watch-folder-archive-{env}",
    visibility_timeout_seconds=0,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

archive_queue_policy = aws.sqs.QueuePolicy("archive-queue-policy",
    queue_url=archive_queue.url,
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[',
        '{"Effect":"Allow","Principal":"*","Action":["sqs:SendMessage"],"Resource":"',
        archive_queue.arn,
        '","Condition":{"ArnEquals":{"aws:SourceArn":"',
        archive_bucket.arn,
        '"}}}',
        ']}'
    ))

# Sync Service Queue
sync_service_queue = aws.sqs.Queue("sync-service-queue",
    name=f"contido-{client}-{env}-sync-service",
    visibility_timeout_seconds=900,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

# File Ingest Service Queue
file_ingest_queue = aws.sqs.Queue("file-ingest-service-queue",
    name=f"contido-{client}-{env}-file-ingest-service",
    visibility_timeout_seconds=900,
    message_retention_seconds=1209600,
    max_message_size=262144,
    sqs_managed_sse_enabled=True,
    tags=tags)

# ============================================================================
# CLOUDFRONT ORIGIN ACCESS IDENTITIES (OAI)
# ============================================================================

mam_proxy_oai = aws.cloudfront.OriginAccessIdentity("mam-proxy-oai",
    comment="access-identity-mam-proxy")

mam_thumbnail_oai = aws.cloudfront.OriginAccessIdentity("mam-thumbnail-oai",
    comment="access-identity-mam-thumbnail")

asset_oai = aws.cloudfront.OriginAccessIdentity("asset-oai",
    comment="access-identity-asset")

# ============================================================================
# S3 BUCKET POLICIES FOR CLOUDFRONT
# ============================================================================

mam_bucket_policy = aws.s3.BucketPolicy("mam-bucket-policy",
    bucket=mam_bucket.id,
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"',
        mam_proxy_oai.iam_arn,
        '"},"Action":"s3:GetObject","Resource":"',
        mam_bucket.arn,
        '/*"},{"Effect":"Allow","Principal":{"AWS":"',
        mam_thumbnail_oai.iam_arn,
        '"},"Action":"s3:GetObject","Resource":"',
        mam_bucket.arn,
        '/*"}]}'
    ))

asset_bucket_policy = aws.s3.BucketPolicy("asset-bucket-policy",
    bucket=asset_bucket.id,
    policy=pulumi.Output.concat(
        '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"',
        asset_oai.iam_arn,
        '"},"Action":"s3:GetObject","Resource":"',
        asset_bucket.arn,
        '/*"}]}'
    ))

# ============================================================================
# CLOUDFRONT DISTRIBUTIONS
# ============================================================================

# MAM Proxy CDN Distribution
mam_proxy_distribution = aws.cloudfront.Distribution("mam-proxy-cdn",
    enabled=True,
    is_ipv6_enabled=True,
    comment=f"Contido {client} Proxy {env}",
    default_root_object="",
    origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=pulumi.Output.concat(mam_bucket.bucket_regional_domain_name),
        origin_id=s3_mam_proxy_origin_id,
        origin_path="/proxy",
        s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
            origin_access_identity=mam_proxy_oai.cloudfront_access_identity_path,
        ),
    )],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=["GET", "HEAD"],
        cached_methods=["GET", "HEAD"],
        target_origin_id=s3_mam_proxy_origin_id,
        compress=True,
        viewer_protocol_policy="redirect-to-https",
        cache_policy_id=cache_policy_id if cache_policy_id else "658327ea-f89d-4fab-a63d-7e88639e58f6",
        origin_request_policy_id=origin_request_policy_id if origin_request_policy_id else "216adef5-5c7f-47e4-b989-5492eafa07d3",
        response_headers_policy_id=response_headers_policy_id if response_headers_policy_id else "",
    ),
    price_class="PriceClass_All",
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none",
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
    ) if not acm_certificate_arn else aws.cloudfront.DistributionViewerCertificateArgs(
        acm_certificate_arn=acm_certificate_arn,
        minimum_protocol_version="TLSv1.2_2021",
        ssl_support_method="sni-only",
    ),
    depends_on=[mam_bucket_policy],
    tags=tags)

# MAM Thumbnail CDN Distribution
mam_thumbnail_distribution = aws.cloudfront.Distribution("mam-thumbnail-cdn",
    enabled=True,
    is_ipv6_enabled=True,
    comment=f"Contido {client} Thumbnail {env}",
    default_root_object="",
    origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=pulumi.Output.concat(mam_bucket.bucket_regional_domain_name),
        origin_id=s3_mam_thumbnail_origin_id,
        origin_path="/thumbnail",
        s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
            origin_access_identity=mam_thumbnail_oai.cloudfront_access_identity_path,
        ),
    )],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=["GET", "HEAD"],
        cached_methods=["GET", "HEAD"],
        target_origin_id=s3_mam_thumbnail_origin_id,
        compress=True,
        viewer_protocol_policy="redirect-to-https",
        cache_policy_id=cache_policy_id if cache_policy_id else "658327ea-f89d-4fab-a63d-7e88639e58f6",
        origin_request_policy_id=origin_request_policy_id if origin_request_policy_id else "216adef5-5c7f-47e4-b989-5492eafa07d3",
        response_headers_policy_id=response_headers_policy_id if response_headers_policy_id else "",
    ),
    price_class="PriceClass_All",
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none",
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
    ) if not acm_certificate_arn else aws.cloudfront.DistributionViewerCertificateArgs(
        acm_certificate_arn=acm_certificate_arn,
        minimum_protocol_version="TLSv1.2_2021",
        ssl_support_method="sni-only",
    ),
    depends_on=[mam_bucket_policy],
    tags=tags)

# Asset CDN Distribution
asset_distribution = aws.cloudfront.Distribution("asset-cdn",
    enabled=True,
    is_ipv6_enabled=True,
    comment=f"Contido {client} Assets {env}",
    default_root_object="",
    origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=pulumi.Output.concat(asset_bucket.bucket_regional_domain_name),
        origin_id=s3_asset_origin_id,
        s3_origin_config=aws.cloudfront.DistributionOriginS3OriginConfigArgs(
            origin_access_identity=asset_oai.cloudfront_access_identity_path,
        ),
    )],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=["GET", "HEAD"],
        cached_methods=["GET", "HEAD"],
        target_origin_id=s3_asset_origin_id,
        compress=True,
        viewer_protocol_policy="redirect-to-https",
        cache_policy_id=cache_policy_id if cache_policy_id else "658327ea-f89d-4fab-a63d-7e88639e58f6",
        origin_request_policy_id=origin_request_policy_id if origin_request_policy_id else "216adef5-5c7f-47e4-b989-5492eafa07d3",
        response_headers_policy_id=response_headers_policy_id if response_headers_policy_id else "",
    ),
    price_class="PriceClass_All",
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="none",
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
    ) if not acm_certificate_arn else aws.cloudfront.DistributionViewerCertificateArgs(
        acm_certificate_arn=acm_certificate_arn,
        minimum_protocol_version="TLSv1.2_2021",
        ssl_support_method="sni-only",
    ),
    depends_on=[asset_bucket_policy],
    tags=tags)

# ============================================================================
# ROUTE53 RECORDS (Optional - only if r53_zone_id is provided)
# ============================================================================

proxy_record = aws.route53.Record("proxy-record",
    zone_id=r53_zone_id,
    name=f"ct{client}proxy{env}",
    type="CNAME",
    ttl=60,
    records=[mam_proxy_distribution.domain_name],
    opts=pulumi.ResourceOptions(depends_on=[mam_proxy_distribution])
) if r53_zone_id else None

thumbnail_record = aws.route53.Record("thumbnail-record",
    zone_id=r53_zone_id,
    name=f"ct{client}thumbnail{env}",
    type="CNAME",
    ttl=60,
    records=[mam_thumbnail_distribution.domain_name],
    opts=pulumi.ResourceOptions(depends_on=[mam_thumbnail_distribution])
) if r53_zone_id else None

asset_record = aws.route53.Record("asset-record",
    zone_id=r53_zone_id,
    name=f"ct{client}assets{env}",
    type="CNAME",
    ttl=60,
    records=[asset_distribution.domain_name],
    opts=pulumi.ResourceOptions(depends_on=[asset_distribution])
) if r53_zone_id else None

# ============================================================================
# LAMBDA FUNCTIONS
# ============================================================================

lambda_sync_service = aws.lambda_.Function("sync-service",
    function_name=f"contido-{client}-{env}-sync-service",
    role=iam_role.arn,
    image_uri=image_uri_sync if image_uri_sync else "placeholder:latest",
    package_type="Image",
    timeout=900,
    memory_size=memory_size,
    ephemeral_storage=aws.lambda_.FunctionEphemeralStorageArgs(
        size=ephemeral_storage_size,
    ),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={},
    ),
    tags=tags) if image_uri_sync else None

lambda_sync_event_mapping = aws.lambda_.EventSourceMapping("sync-service-event",
    event_source_arn=sync_service_queue.arn,
    function_name=lambda_sync_service.name if lambda_sync_service else "",
    batch_size=batch_size,
    opts=pulumi.ResourceOptions(depends_on=[lambda_sync_service]) if lambda_sync_service else None
) if lambda_sync_service else None

lambda_file_ingest_service = aws.lambda_.Function("file-ingest-service",
    function_name=f"contido-{client}-{env}-file-ingest-service",
    role=iam_role.arn,
    image_uri=image_uri_ingest if image_uri_ingest else "placeholder:latest",
    package_type="Image",
    timeout=900,
    memory_size=memory_size,
    ephemeral_storage=aws.lambda_.FunctionEphemeralStorageArgs(
        size=ephemeral_storage_size,
    ),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={},
    ),
    tags=tags) if image_uri_ingest else None

lambda_file_ingest_event_mapping = aws.lambda_.EventSourceMapping("file-ingest-event",
    event_source_arn=file_ingest_queue.arn,
    function_name=lambda_file_ingest_service.name if lambda_file_ingest_service else "",
    batch_size=batch_size,
    opts=pulumi.ResourceOptions(depends_on=[lambda_file_ingest_service]) if lambda_file_ingest_service else None
) if lambda_file_ingest_service else None

# ============================================================================
# OUTPUTS
# ============================================================================

pulumi.export("iam_userbe_name", iam_userbe.name)
pulumi.export("iam_userfe_name", iam_userfe.name)
pulumi.export("iam_aspera_name", iam_aspera.name)
pulumi.export("upload_bucket_name", upload_bucket.id)
pulumi.export("mam_bucket_name", mam_bucket.id)
pulumi.export("asset_bucket_name", asset_bucket.id)
pulumi.export("archive_bucket_name", archive_bucket.id)
pulumi.export("edit_bucket_name", edit_bucket.id)
pulumi.export("proxy_cdn_domain", mam_proxy_distribution.domain_name)
pulumi.export("thumbnail_cdn_domain", mam_thumbnail_distribution.domain_name)
pulumi.export("asset_cdn_domain", asset_distribution.domain_name)
pulumi.export("upload_queue_url", upload_queue.url)
pulumi.export("mam_restore_queue_url", mam_restore_queue.url)
pulumi.export("transfer_queue_url", transfer_queue.url)
pulumi.export("ingest_proxy_queue_url", ingest_proxy_queue.url)
pulumi.export("transcoding_start_queue_url", transcoding_start_queue.url)
pulumi.export("client_delivery_queue_url", client_delivery_queue.url)
pulumi.export("archive_queue_url", archive_queue.url)
pulumi.export("sync_service_queue_url", sync_service_queue.url)
pulumi.export("file_ingest_queue_url", file_ingest_queue.url)
pulumi.export("sync_lambda_name", lambda_sync_service.function_name if lambda_sync_service else "Not configured")
pulumi.export("file_ingest_lambda_name", lambda_file_ingest_service.function_name if lambda_file_ingest_service else "Not configured")
pulumi.export("iam_role_name", iam_role.name)
pulumi.export("resources_access_policy_name", resources_access_policy.name)
pulumi.export("secret_manager_policy_name", secret_manager_policy.name)
pulumi.export("lambda_basic_policy_name", lambda_basic_policy.name)
pulumi.export("fe_asset_policy_name", userfe_policy.name)
pulumi.export("cdn_invalidation_policy_name", cdn_invalidation_policy.name)
pulumi.export("aspera_policy_name", useraspera_policy.name)
