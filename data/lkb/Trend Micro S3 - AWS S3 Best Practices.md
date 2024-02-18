# AWS S3 Best Practices | Trend Micro

AWS Simple Storage Service (S3) is a storage device for the Internet. It has a web service that makes storage and retrieval simple at any time, from anywhere on the web, regardless of the amount of data. S3 is designed to make web-scale computing simple for developers by providing highly scalable, fast, reliable, and inexpensive data storage infrastructure.

Trend Micro Cloud One™ – Conformity monitors Amazon S3 with the following rules:

- [Amazon Macie Finding Statistics for S3](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/macie-finding-statistics-for-s3.html)
  - Capture summary statistics about Amazon Macie security findings on a per-S3 bucket basis.
  
- [Configure Different S3 Bucket for Server Access Logging Storage](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/server-access-log-storage-different-bucket.html)
  - Ensure that Amazon S3 Server Access Logging uses a different bucket for storing access logs.
  
- [Configure S3 Object Ownership](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/enforce-s3-object-ownership.html)
  - Ensure that S3 Object Ownership is configured to allow you to take ownership of S3 objects.
  
- [DNS Compliant S3 Bucket Names](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/dns-compliant-buckets-names.html)
  - Ensure that Amazon S3 buckets always use DNS-compliant bucket names.
  
- [Deny S3 Log Delivery Group Write Permission on the Source Bucket](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/deny-log-delivery-group-write-permission.html)
  - Ensure that the S3 Log Delivery Group write permissions are denied for the S3 source bucket.
  
- [Enable S3 Block Public Access for AWS Accounts](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/account-public-access-block.html)
  - Ensure that Amazon S3 public access is blocked at the AWS account level for data protection.
  
- [Enable S3 Block Public Access for S3 Buckets](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/bucket-public-access-block.html)
  - Ensure that Amazon S3 public access is blocked at the S3 bucket level for data protection.
  
- [Enable S3 Bucket Keys](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/configure-s3-bucket-keys.html)
  - Ensure that Amazon S3 buckets are using S3 bucket keys to optimize service costs.
  
- [S3 Bucket Authenticated Users 'FULL_CONTROL' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-authenticated-users-full-control-access.html)
  - Ensure that S3 buckets do not allow FULL_CONTROL access to AWS authenticated users via ACLs.
  
- [S3 Bucket Authenticated Users 'READ' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-authenticated-users-read-access.html)
  - Ensure that S3 buckets do not allow READ access to AWS authenticated users via ACLs.
  
- [S3 Bucket Authenticated Users 'READ_ACP' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-authenticated-users-read-acp-access.html)
  - Ensure that S3 buckets do not allow READ_ACP access to AWS authenticated users via ACLs.
  
- [S3 Bucket Authenticated Users 'WRITE' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-authenticated-users-write-access.html)
  - Ensure that S3 buckets do not allow WRITE access to AWS authenticated users via ACLs.
  
- [S3 Bucket Authenticated Users 'WRITE_ACP' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-authenticated-users-write-acp-access.html)
  - Ensure that S3 buckets do not allow WRITE_ACP access to AWS authenticated users via ACLs.
  
- [S3 Bucket Default Encryption (Deprecated)](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/bucket-default-encryption.html)
  - Ensure that encryption at rest is enabled for your Amazon S3 buckets and their data.
  
- [S3 Bucket Logging Enabled](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-logging-enabled.html)
  - Ensure S3 bucket access logging is enabled for security and access audits.
  
- [S3 Bucket MFA Delete Enabled](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-mfa-delete-enabled.html)
  - Ensure S3 buckets have an MFA-Delete policy to prevent deletion of files without an MFA token.
  
- [S3 Bucket Public 'FULL_CONTROL' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-public-full-control-access.html)
  - Ensure that your Amazon S3 buckets are not publicly exposed to the Internet.
  
- [S3 Bucket Public 'READ' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-public-read-access.html)
  - Ensure that S3 buckets do not allow public READ access via Access Control Lists (ACLs).
  
- [S3 Bucket Public 'READ_ACP' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-public-read-acp-access.html)
  - Ensure that S3 buckets do not allow public READ_ACP access via Access Control Lists (ACLs).
  
- [S3 Bucket Public 'WRITE' ACL Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-public-write-access.html)
  - Ensure S3 buckets don’t allow public WRITE ACL access
  
- [S3 Bucket Public 'WRITE_ACP' Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-public-write-acp-access.html)
  - Ensure that S3 buckets do not allow public WRITE_ACP access via Access Control Lists (ACLs).
  
- [S3 Bucket Public Access Via Policy](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-public-access-via-policy.html)
  - Ensure that Amazon S3 buckets do not allow public access via bucket policies.
  
- [S3 Bucket Versioning Enabled](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-bucket-versioning-enabled.html)
  - Ensure S3 bucket versioning is enabled for an additional level of data protection.
  
- [S3 Buckets Encrypted with Customer-Provided CMKs](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/encrypted-with-kms-customer-master-keys.html)
  - Ensure that Amazon S3 buckets are encrypted with customer-provided KMS CMKs.
  
- [S3 Buckets Lifecycle Configuration](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/lifecycle-configuration.html)
  - Ensure that AWS S3 buckets utilize lifecycle configurations to manage S3 objects during their lifetime.
  
- [S3 Buckets with Website Hosting Configuration Enabled](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/buckets-with-website-configurations.html)
  - Ensure that the S3 buckets with website configuration are regularly reviewed (informational).
  
- [S3 Configuration Changes](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/configuration-changes.html)
  - AWS S3 configuration changes have been detected within your Amazon Web Services account.
  
- [S3 Cross Account Access](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/s3-cross-account-access.html)
  - Ensure that S3 buckets do not allow unknown cross-account access via bucket policies.
  
- [S3 Object Lock](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/object-lock.html)
  - Ensure that S3 buckets use Object Lock for data protection and/or regulatory compliance.
  
- [S3 Transfer Acceleration](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/transfer-acceleration.html)
  - Ensure that S3 buckets use the Transfer Acceleration feature for faster data transfers.
  
- [Secure Transport](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/secure-transport.html)
  - Ensure AWS S3 buckets enforce SSL to secure data in transit.
  
- [Server Side Encryption](https://trendmicro.com/cloudoneconformity/knowledge-base/aws/S3/server-side-encryption.html)
  - Ensure AWS S3 buckets enforce Server-Side Encryption (SSE)