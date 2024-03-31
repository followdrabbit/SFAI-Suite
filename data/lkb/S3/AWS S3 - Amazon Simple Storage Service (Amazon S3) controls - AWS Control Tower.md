# Amazon Simple Storage Service (Amazon S3) controls - AWS Control Tower

###### Topics

- [\[CT.S3.PR.1\] Require an Amazon S3 bucket to have block public access settings configured](#ct-s3-pr-1-description)
- [\[CT.S3.PR.2\] Require an Amazon S3 bucket to have server access logging configured](#ct-s3-pr-2-description)
- [\[CT.S3.PR.3\] Require an Amazon S3 buckets to have versioning configured and a lifecycle policy](#ct-s3-pr-3-description)
- [\[CT.S3.PR.4\] Require an Amazon S3 bucket to have event notifications configured](#ct-s3-pr-4-description)
- [\[CT.S3.PR.5\] Require that an Amazon S3 bucket does not manage user access with an access control list (ACL)](#ct-s3-pr-5-description)
- [\[CT.S3.PR.6\] Require an Amazon S3 bucket to have lifecycle policies configured](#ct-s3-pr-6-description)
- [\[CT.S3.PR.8\] Require that Amazon S3 bucket requests use Secure Socket Layer](#ct-s3-pr-8-description)
- [\[CT.S3.PR.9\] Require that an Amazon S3 bucket has S3 Object Lock activated](#ct-s3-pr-9-description)
- [\[CT.S3.PR.10\] Require an Amazon S3 bucket to have server-side encryption configured using an AWS KMS key](#ct-s3-pr-10-description)
- [\[CT.S3.PR.11\] Require an Amazon S3 bucket to have versioning enabled](#ct-s3-pr-11-description)
- [\[CT.S3.PR.12\] Require an Amazon S3 access point to have a Block Public Access (BPA) configuration with all options set to true](#ct-s3-pr-12-description)

## \[CT.S3.PR.1\] Require an Amazon S3 bucket to have block public access settings configured

This control checks whether your Amazon Simple Storage Service (Amazon S3) bucket has a bucket-level Block Public Access (BPA) configuration.

- **Control objective:** Limit network access
- **Implementation:** AWS CloudFormation Guard Rule
- **Control behavior:** Proactive
- **Resource types:** `AWS::S3::Bucket`
- **AWS CloudFormation guard rule:** [CT.S3.PR.1 rule specification](#ct-s3-pr-1-rule)

**Details and examples**

- For details about the PASS, FAIL, and SKIP behaviors associated with this control, see the: [CT.S3.PR.1 rule specification](#ct-s3-pr-1-rule)
- For examples of PASS and FAIL CloudFormation Templates related to this control, see: [CT.S3.PR.1 example templates](#ct-s3-pr-1-templates)

**Explanation**

Block Public Access at the Amazon S3 bucket level provides controls to ensure that objects never have public access. Public access is granted to buckets and objects through access control lists (ACLs), bucket policies, or both.

Unless you intend to have your S3 buckets publicly accessible, you should configure the bucket level Amazon S3 Block Public Access feature.

###### Usage considerations

- This control is incompatible with Amazon S3 buckets that require a public access configuration.

### Remediation for rule failure

The parameters `BlockPublicAcls`, `BlockPublicPolicy`, `IgnorePublicAcls`, `RestrictPublicBuckets` must be set to true under the bucket-level `PublicAccessBlockConfiguration`.

The examples that follow show how to implement this remediation.

#### Amazon S3 Bucket - Example

Amazon S3 bucket with a bucket level Block Public Access configuration that ensures objects never have public access. The example is shown in JSON and in YAML.

**JSON example**

```json
{
    "S3Bucket": {
        "Type": "AWS::S3::Bucket",
        "Properties": {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": true,
                "BlockPublicPolicy": true,
                "IgnorePublicAcls": true,
                "RestrictPublicBuckets": true
            }
        }
    }
}
```

**YAML example**

```YAML

S3Bucket:
  Type: AWS::S3::Bucket
  Properties:
    PublicAccessBlockConfiguration:
      BlockPublicAcls: true
      BlockPublicPolicy: true
      IgnorePublicAcls: true
      RestrictPublicBuckets: true
```

### CT.S3.PR.1 rule specification

```plaintext
# ###################################
##       Rule Specification        ##
#####################################
# 
# Rule Identifier:
#   s3_bucket_level_public_access_prohibited_check
# 
# Description:
#   Checks whether Amazon Simple Storage Service (Amazon S3) buckets have a bucket-level Block Public Access (BPA)
#   configuration.
# 
# Reports on:
#   AWS::S3::Bucket
# 
# Evaluates:
#   AWS CloudFormation, AWS CloudFormation hook
# 
# Rule Parameters:
#   None
# 
# Scenarios:
#   Scenario: 1
#     Given: The input document is an AWS CloudFormation or CloudFormation hook document
#       And: The input document does not contain any Amazon S3 bucket resources
#      Then: SKIP
#   Scenario: 2
#     Given: The input document is an AWS CloudFormation or CloudFormation hook document
#       And: The input document contains an Amazon S3 bucket resource
#       And: 'PublicAccessBlockConfiguration' has not been provided
#      Then: FAIL
#   Scenario: 3
#     Given: The input document is an AWS CloudFormation or CloudFormation hook document
#       And: The input document contains an Amazon S3 bucket resource
#       And: 'PublicAccessBlockConfiguration' has been provided
#       And: 'BlockPublicAcls' or 'BlockPublicPolicy' or 'IgnorePublicAcls' or 'RestrictPublicBuckets'
#            have not been provided
#      Then: FAIL
#   Scenario: 4
#     Given: The input document is an AWS CloudFormation or CloudFormation hook document
#       And: The input document contains an Amazon S3 bucket Resource
#       And: 'PublicAccessBlockConfiguration' has been provided
#       And: Any of 'BlockPublicAcls' or 'BlockPublicPolicy' or 'IgnorePublicAcls' or 'RestrictPublicBuckets'
#            have been set to a value other than bool(true) (e.g. bool(false), str(false), other)
#      Then: FAIL
#   Scenario: 5
#     Given: The input document is an AWS CloudFormation or CloudFormation hook document
#       And: The input document contains an Amazon S3 bucket Resource
#       And: 'PublicAccessBlockConfiguration' has been provided
#       And: 'BlockPublicAcls' or 'BlockPublicPolicy' or 'IgnorePublicAcls' or 'RestrictPublicBuckets'
#            have all been set to bool(true)
#      Then: PASS
```

### CT.S3.PR.1 example templates

You can view examples of the PASS and FAIL test artifacts for the AWS Control Tower proactive controls.

**PASS Example** - Use this template to verify a compliant resource creation.

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
```


**FAIL Example** - Use this template to verify that the control prevents non-compliant resource creation.

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      PublicAccessBlockConfiguration:
        BlockPublicAcls: false
        BlockPublicPolicy: false
        IgnorePublicAcls: false
        RestrictPublicBuckets: false
```