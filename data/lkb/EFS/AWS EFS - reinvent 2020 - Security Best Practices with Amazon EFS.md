# Security Best Practices with Amazon EFS

**Presenter:** Vasily Pantyukhin, Senior Solutions Architect, Storage, AWS

## Amazon EFS Overview

- Amazon EFS is a fully managed, highly reliable, cost-optimized, cloud-native file system.
- Supports the AWS shared responsibility model, where AWS is responsible for the security of the cloud infrastructure, and the customer is responsible for security in the cloud.

## Security Best Practices

### Control File and Directory Access

- Use numeric UIDs/GIDs to restrict file/directory access with POSIX.
- Employ access points to enforce user identity and root directory, overriding UIDs/GIDs provided by the NFS client.

### Control Network Access

- Mount targets are Elastic Network Interfaces (ENIs), and network access can be controlled with security groups.

### Encrypt Data

- Support for encryption in transit (TLS v1.2) and at rest (AES-256).

### Control Client and API Access

- Use identity-based and resource-based policies for access restriction.
- Predefined and customer-managed policies are available for fine-grained access control.

### File System Policy Options

- File system policy options include anonymous access, permissions for individual IAM roles, and access restriction with specific access points.

### Reinforce Encryption

- Policies to enforce encryption in transit and at rest.

## Compliance

- Amazon EFS complies with various compliance standards, including HIPAA, GDPR, PCI-DSS, SOC, ISO, and more.

## Key Takeaways

- Use access points, even if a single application per file system.
- Always control network access with security groups.
- Always enable encryption in transit and at rest.
- Use IAM to restrict access to in-cloud resources.
