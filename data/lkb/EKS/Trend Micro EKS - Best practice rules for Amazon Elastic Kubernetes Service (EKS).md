## Best practice rules for Amazon Elastic Kubernetes Service (EKS)

Trend Micro Cloud One™ – Conformity monitors Amazon Elastic Kubernetes Service (EKS) with the following rules:

* [Check for the CoreDNS Add-On Version](/cloudoneconformity-staging/knowledge-base/aws/EKS/eks-aws-managed-core-dns-addon.html)
  
  Ensure that the CoreDNS add-on version matches the EKS cluster's Kubernetes version.
  
* [Disable Remote Access to EKS Cluster Node Groups](/cloudoneconformity-staging/knowledge-base/aws/EKS/eks-node-group-remote-access.html)
  
  Ensure that remote access to EKS cluster node groups is disabled.
  
* [EKS Cluster Endpoint Public Access](/cloudoneconformity-staging/knowledge-base/aws/EKS/endpoint-access.html)
  
  Ensure that AWS EKS cluster endpoint access isn't public and prone to security risks.
  
* [EKS Cluster Node Group IAM Role Policies](/cloudoneconformity-staging/knowledge-base/aws/EKS/worker-nodes-managed-policies.html)
  
  Ensure that EKS Cluster node groups are using appropriate permissions.
  
* [EKS Security Groups](/cloudoneconformity-staging/knowledge-base/aws/EKS/security-groups.html)
  
  Ensure that AWS EKS security groups are configured to allow incoming traffic only on TCP port 443.
  
* [Enable CloudTrail Logging for Kubernetes API Calls](/cloudoneconformity-staging/knowledge-base/aws/EKS/eks-logging-kubes-api-calls.html)
  
  Ensure that all Kubernetes API calls are logged using Amazon CloudTrail.
  
* [Enable Envelope Encryption for EKS Kubernetes Secrets](/cloudoneconformity-staging/knowledge-base/aws/EKS/enable-envelope-encryption.html)
  
  Ensure that envelope encryption of Kubernetes secrets using Amazon KMS is enabled.
  
* [Kubernetes Cluster Logging](/cloudoneconformity-staging/knowledge-base/aws/EKS/cluster-logging.html)
  
  Ensure that EKS control plane logging is enabled for your Amazon EKS clusters.
  
* [Kubernetes Cluster Version](/cloudoneconformity-staging/knowledge-base/aws/EKS/kubernetes-version.html)
  
  Ensure that the latest version of Kubernetes is installed on your Amazon EKS clusters.
  
* [Monitor Amazon EKS Configuration Changes](/cloudoneconformity-staging/knowledge-base/aws/EKS/configuration-changes.html)
  
  Amazon EKS configuration changes have been detected within your Amazon Web Services account.
  
* [Use AWS-managed policy to Manage Networking Resources](/cloudoneconformity-staging/knowledge-base/aws/EKS/eks-iam-managed-policy-networking.html)
  
  Ensure that EKS cluster node groups implement the "AmazonEKS_CNI_Policy" managed policy.
  
* [Use AWS-managed policy to access Amazon ECR Repositories](/cloudoneconformity-staging/knowledge-base/aws/EKS/managed-policy-ecr-access.html)
  
  Ensure that EKS cluster node groups implement the "AmazonEC2ContainerRegistryReadOnly" managed policy.
  
* [Use AWS-managed policy to manage AWS resources](/cloudoneconformity-staging/knowledge-base/aws/EKS/eks-aws-managed-iam-policy.html)
  
  Ensure that Amazon EKS clusters implement the "AmazonEKSClusterPolicy" managed policy.
  
* [Use OIDC Provider for Authenticating Kubernetes API Calls](/cloudoneconformity-staging/knowledge-base/aws/EKS/eks-oidc-provider-api-calls.html)
  
  Ensure that Amazon EKS clusters are using an OpenID Connect (OIDC) provider.
