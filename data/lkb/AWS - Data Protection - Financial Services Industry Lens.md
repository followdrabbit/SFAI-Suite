# Data Protection - Financial Services Industry Lens

FSISEC13: How do you classify your data?

Financial services institutions use data classification to make determinations about safeguarding sensitive or critical data with appropriate levels of protection. Regardless of whether data is processed or stored in on premises systems or the cloud, data classification is a starting point for determining the appropriate level of controls for the confidentiality, integrity, and availability of data based on risk to the organization. It is the customer’s responsibility to classify their data and implement appropriate controls within their cloud environment (e.g., encryption).The security controls that AWS implements within its infrastructure and service offerings can be used by customers to meet the most sensitive data requirements.

## Tag AWS services based on data classification

Data classification best practices start with clearly defined data classification tiers and requirements, which meet your organizational, legal, and compliance standards.

Use tags on AWS resources based on the data classification framework to implement compliance with your data governance program. Tagging in this context can be used for automation such as enabling and validating data encryption, retention, and archiving.

## Restrict access based on classification

Use these resource tags and IAM policies, along with AWS KMS or CloudHSM, to define and implement your own policies that enforce protections based on data classification. For example, if you have S3 buckets or EC2 instances that contain or process highly critical and confidential data, tag them with a tag `DataClassification=CRITICAL` and automate data residing in them to be encrypted with AWS KMS. You can then define levels of access to those KMS encryption keys through key policies to ensure that only appropriate services have access to the sensitive content.

## Leverage automated detection of confidential data

While many types of data can be classified as highly confidential, Personally Identifiable Information (PII) has long received regulatory attention. AWS offers several services and features that can facilitate an organization’s implementation and automation of a data classification scheme. Amazon Macie can help you inventory and classify your sensitive and business-critical data stored in the cloud. Amazon Macie recognizes sensitive data such as personally identifiable information (PII) or intellectual property, and provides you with dashboards and alerts that give visibility into how this data is being accessed or moved.

## Monitor/audit usage of data based on classification

**Amazon Macie** allows you to automate data protection workflows by integrating with your Security Information and Event Management (SIEM) system and Managed Security Service Provider (MSSP) solutions using CloudWatch Events. Security and compliance use cases such as alert handling, compliance ruleset creation and modifications, reporting and configurations for content in Amazon S3, and detecting user authentication and access patterns through CloudTrail can be solved with this integration. Amazon Macie also gives you the ability to easily define and customize automated remediation actions, such as resetting access control lists or triggering password reset policies.

Refer to the [AWS Data Classification whitepaper](https://docs.aws.amazon.com/whitepapers/latest/data-classification/data-classification.html) for additional best practices.

## Managing data loss prevention

FSISEC14: How are you handling data loss prevention in the cloud environment?

AWS offers a broad set of tools and services to help implement effective data protection strategies, which include IAM to prevent unauthorized access, Key Management Service (KMS), CloudHSM to manage encryption, CloudTrail to monitor data access activities, and Lambda functions to perform remediation actions in real time and Amazon Macie to monitor access patterns using machine learning.

### Use Fully Qualified Domain Name (FQDN) ingress and egress filters

Specifying policies by IP may not be practical because domain names can often be translated to many different IP addresses, and maintaining security groups at each egress point can be challenging. Filtering outbound traffic by an expected list of domain names can be an efficient way to secure egress traffic from a VPC because the hostnames of these services are typically known at deployment, and the list of hosts that need to be accessed by an application are not extensive and rarely change.

Filtering traffic by a list of domain names enables companies to centralize the maintenance and deployment of rules. Use a third-party solution to implement highly available, secure FQDN Egress Filtering service.

### Use VPC Endpoints and VPC Endpoint Policies for network perimeter security

VPC endpoints enable you to privately connect your VPC to supported regional services without requiring public IP addresses. When you create an endpoint, you can also attach an endpoint policy to it. This policy controls access to the service you are connecting to. VPC endpoint policies can prevent access to AWS services with non-corporate credentials by using conditions such as AWS:PrincipalAccount, AWS:PrincipalOrgId or AWS:PrincipalOrgPaths in the endpoint policy. These conditions ensure that only corporate credentials are used within the VPC to connect to your AWS regional services. Also, you can use limit access to only specific AWS resources such as specific Amazon S3 buckets through the endpoint with endpoint policies.

### Enforce deny public access for Amazon S3

Use data classification best practices to identify public and non-public data. For non-public data stored in Amazon S3, make sure public access is denied. You can use the Amazon S3 Block Public Access settings on each bucket or at an account level to make sure that existing and newly created resources block bucket policies or ACLs do not allow public access. You can also define SCPs to prevent users from modifying this setting. Use AWS Config and Lambda to detect and remediate if S3 buckets are publicly accessible.

### Enforce encryption

Encryption, both in transit and at rest, is another best practice to ensure the security of the data, regardless of the reason. Enabling encryption on most AWS services is simply a matter of selecting it at deployment. Use AWS Config to alert when a deployment has been made that does not meet your policy.

### Configure encryption by default for Amazon S3

To avoid unintentionally storing data unencrypted, encryption for data at rest must be enabled by default. This is particularly relevant for object-based storage using Amazon S3. Set default encryption on a S3 bucket to turn on encryption by default for all objects stored in that bucket (keep in mind that any objects already stored in the bucket when encryption was turned on remain unencrypted). Use CMK-based encryption as described in FSISEC15.

### Monitor VPC Flow Logs for abnormal traffic patterns

Use VPC Flow Logs to watch for abnormal and unexpected outbound connection requests, which could be an indication of unauthorized exfiltration of data. Amazon GuardDuty analyzes VPC Flow Logs, AWS CloudTrail event logs, and DNS logs to identify unexpected and potentially malicious activity within your AWS environment. For example, GuardDuty can detect compromised EC2 instances communicating with known command-and-control servers.

### Audit the use of encryption in Amazon S3

In addition to setting the default encryption behavior for S3 buckets, it is important to perform periodic audits of the encryption status through automated surveillance reports. S3 Inventory reports include encryption status in its list of objects and their metadata. This is a scheduled report provided on a daily or weekly basis for a bucket or prefix. The addition of encryption status to S3 inventory allows you to see how objects are encrypted for compliance auditing or other purposes.

S3 Inventory reports can be encrypted as an extra measure of protection to prevent the objects metadata being disclosed to unauthorized parties (for example, names of files can be confidential information).