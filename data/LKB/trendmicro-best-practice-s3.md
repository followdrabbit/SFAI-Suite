# Best practice rules for Amazon S3

AWS Simple Storage Service (S3) is a storage device for the Internet. It has a web service that makes storage and retrieval simple at any time, from anywhere on the web, regardless of the amount of data. S3 is designed to make web-scale computing simple for developers by providing highly scalable, fast, reliable and inexpensive data storage infrastructure.

Trend Micro Cloud One™ – Conformity monitors Amazon S3 with the following rules:

 - Amazon Macie Finding Statistics for S3
 - Capture summary statistics about Amazon Macie security findings on a per-S3 bucket basis.

 - Configure Different S3 Bucket for Server Access Logging Storage
 - Ensure that Amazon S3 Server Access Logging uses a different bucket for storing access logs.

 - Configure S3 Object Ownership
 - Ensure that S3 Object Ownership is configured to allow you to take ownership of S3 objects.

 - DNS Compliant S3 Bucket Names
 - Ensure that Amazon S3 buckets always use DNS-compliant bucket names.

 - Deny S3 Log Delivery Group Write Permission on the Source Bucket
 - Ensure that the S3 Log Delivery Group write permissions are denied for the S3 source bucket.

 - Enable S3 Block Public Access for AWS Accounts
 - Ensure that Amazon S3 public access is blocked at the AWS account level for data protection.

 - Enable S3 Block Public Access for S3 Buckets
 - Ensure that Amazon S3 public access is blocked at the S3 bucket level for data protection.

 - Enable S3 Bucket Keys
 - Ensure that Amazon S3 buckets are using S3 bucket keys to optimize service costs.

 - S3 Bucket Authenticated Users 'FULL_CONTROL' Access
 - Ensure that S3 buckets do not allow FULL_CONTROL access to AWS authenticated users via ACLs.

 - S3 Bucket Authenticated Users 'READ' Access
 - Ensure that S3 buckets do not allow READ access to AWS authenticated users via ACLs.

 - S3 Bucket Authenticated Users 'READ_ACP' Access
 - Ensure that S3 buckets do not allow READ_ACP access to AWS authenticated users via ACLs.

 - S3 Bucket Authenticated Users 'WRITE' Access
 - Ensure that S3 buckets do not allow WRITE access to AWS authenticated users via ACLs.

 - S3 Bucket Authenticated Users 'WRITE_ACP' Access
 - Ensure that S3 buckets do not allow WRITE_ACP access to AWS authenticated users via ACLs.

 - S3 Bucket Default Encryption (Deprecated)
 - Ensure that encryption at rest is enabled for your Amazon S3 buckets and their data.

 - S3 Bucket Logging Enabled
 - Ensure S3 bucket access logging is enabled for security and access audits.

 - S3 Bucket MFA Delete Enabled
 - Ensure S3 buckets have an MFA-Delete policy to prevent deletion of files without an MFA token.

 - S3 Bucket Public 'FULL_CONTROL' Access
 - Ensure that your Amazon S3 buckets are not publicly exposed to the Internet.

 - S3 Bucket Public 'READ' Access
 - Ensure that S3 buckets do not allow public READ access via Access Control Lists (ACLs).

 - S3 Bucket Public 'READ_ACP' Access
 - Ensure that S3 buckets do not allow public READ_ACP access via Access Control Lists (ACLs).

 - S3 Bucket Public 'WRITE' ACL Access
 - Ensure S3 buckets don’t allow public WRITE ACL access.
 
 - S3 Bucket Public 'WRITE_ACP' Access
 - Ensure that S3 buckets do not allow public WRITE_ACP access via Access Control Lists (ACLs).

 - S3 Bucket Public Access Via Policy
 - Ensure that Amazon S3 buckets do not allow public access via bucket policies.

 - S3 Bucket Versioning Enabled
 - Ensure S3 bucket versioning is enabled for additional level of data protection.

 - S3 Buckets Encrypted with Customer-Provided CMKs
 - Ensure that Amazon S3 buckets are encrypted with customer-provided KMS CMKs.

 - S3 Buckets Lifecycle Configuration
 - Ensure that AWS S3 buckets utilize lifecycle configurations to manage S3 objects during their lifetime.

 - S3 Buckets with Website Hosting Configuration Enabled
 - Ensure that the S3 buckets with website configuration are regularly reviewed (informational).

 - S3 Configuration Changes
 - AWS S3 configuration changes have been detected within your Amazon Web Services account.

 - S3 Cross Account Access
 - Ensure that S3 buckets do not allow unknown cross-account access via bucket policies.

 - S3 Object Lock
 - Ensure that S3 buckets use Object Lock for data protection and/or regulatory compliance.

 - S3 Transfer Acceleration
 - Ensure that S3 buckets use the Transfer Acceleration feature for faster data transfers.

 - Secure Transport
 - Ensure AWS S3 buckets enforce SSL to secure data in transit.

 - Server Side Encryption
 - Ensure AWS S3 buckets enforce Server-Side Encryption (SSE)