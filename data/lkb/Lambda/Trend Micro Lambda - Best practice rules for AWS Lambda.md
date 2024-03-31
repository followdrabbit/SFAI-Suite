## Best practice rules for AWS Lambda

Trend Micro Cloud One™ – Conformity monitors AWS Lambda with the following rules:

* [Check Lambda Function URL Not in Use](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-function-url.html)
  Check your Amazon Lambda functions are not using function URLs.

* [Check for Missing Execution Role](/cloudoneconformity-staging/knowledge-base/aws/Lambda/referencing-missing-execution-role.html)
  Ensure that Amazon Lambda functions are referencing active execution roles.

* [Enable Code Signing](/cloudoneconformity-staging/knowledge-base/aws/Lambda/enable-code-signing.html)
  Ensure that Code Signing is enabled for Amazon Lambda functions.

* [Enable Dead Letter Queue for Lambda Functions](/cloudoneconformity-staging/knowledge-base/aws/Lambda/enable-dead-letter-queue.html)
  Ensure there is a Dead Letter Queue configured for each Lambda function available in your AWS account.

* [Enable Encryption at Rest for Environment Variables using Customer Master Keys](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-encrypted-with-cmk.html)
  Ensure that Lambda environment variables are encrypted at rest with Customer Master Keys (CMKs) to gain full control over data encryption/decryption

* [Enable Encryption in Transit for Environment Variables](/cloudoneconformity-staging/knowledge-base/aws/Lambda/encryption-environment-variables.html)
  Ensure that encryption in transit is enabled for the Lambda environment variables that store sensitive information.

* [Enable Enhanced Monitoring for Lambda Functions](/cloudoneconformity-staging/knowledge-base/aws/Lambda/enable-enhanced-monitoring.html)
  Ensure that your Amazon Lambda functions are configured to use enhanced monitoring.

* [Enable IAM Authentication for Lambda Function URLs](/cloudoneconformity-staging/knowledge-base/aws/Lambda/iam-auth-function-url.html)
  Ensure that IAM authorization is enabled for your Lambda function URLs.

* [Enable and Configure Reserved Concurrency](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-function-reserved-concurrency.html)
  Ensure that your Amazon Lambda functions are configured to use reserved concurrency.

* [EnableProvisionedConcurrency](/cloudoneconformity-staging/knowledge-base/aws/Lambda/enable-provisioned-concurrency.html)
  Ensure that your Amazon Lambda functions are configured to use provisioned concurrency.

* [Function Exposed](/cloudoneconformity-staging/knowledge-base/aws/Lambda/function-exposed.html)
  Ensure that your Amazon Lambda functions aren't exposed to everyone.

* [Function in Private Subnet](/cloudoneconformity-staging/knowledge-base/aws/Lambda/function-private-subnet.html)
  Ensure that your Amazon Lambda functions are configured to use private subnets.

* [Functions with Admin Privileges](/cloudoneconformity-staging/knowledge-base/aws/Lambda/function-with-admin-privileges.html)
  Ensure there are no Lambda functions with admin privileges within your AWS account.

* [Lambda Cross Account Access](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-cross-account-access.html)
  Ensure AWS Lambda functions don't allow unknown cross account access via permission policies.

* [Lambda Function Execution Roles with Inline Policies](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-funcion-iam-role-inline-policy.html)
  Ensure that IAM execution roles configured for Lambda functions are not using inline policies.

* [Lambda Using Latest Runtime Environment](/cloudoneconformity-staging/knowledge-base/aws/Lambda/runtime-environment.html)
  Ensure that the latest version of the runtime environment is used for your AWS Lambda functions.

* [Lambda Using Supported Runtime Environment](/cloudoneconformity-staging/knowledge-base/aws/Lambda/supported-runtime-environment.html)
  Ensure the AWS Lambda function runtime version is currently supported.

* [Tracing Enabled](/cloudoneconformity-staging/knowledge-base/aws/Lambda/tracing.html)
  Ensure that tracing (Lambda support for Amazon X-Ray service) is enabled for your AWS Lambda functions.

* [Use AWS-Managed Policies for Lambda Function Execution Roles](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-aws-managed-role.html)
  Ensure that IAM execution roles configured for Lambda functions are using AWS-managed policies.

* [Use Customer-Managed Policies for Lambda Function Execution Roles](/cloudoneconformity-staging/knowledge-base/aws/Lambda/lambda-iam-role-user-managed.html)
  Ensure that IAM execution roles configured for Lambda functions are using customer-managed policies.

* [Using An IAM Role For More Than One Lambda Function](/cloudoneconformity-staging/knowledge-base/aws/Lambda/sharing-an-iam-role-within-more-than-one-lambda-function.html)
  Ensure that Lambda functions don't share the same IAM execution role.

* [VPC Access for AWS Lambda Functions](/cloudoneconformity-staging/knowledge-base/aws/Lambda/function-in-vpc.html)
  Ensure that your Amazon Lambda functions have access to VPC-only resources.
