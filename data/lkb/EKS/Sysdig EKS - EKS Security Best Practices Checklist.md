# EKS Security Best Practices Checklist

## Introduction to Amazon Elastic Kubernetes Service

Amazon Elastic Kubernetes Service (Amazon EKS) is a managed service that allows you to run Kubernetes on AWS without having to install, administer, or maintain your control plane or [Kubernetes nodes](/learn-cloud-native/kubernetes-101/what-is-a-kubernetes-node/). Kubernetes is an open-source platform for automating containerized application deployment, scaling, and administration. Using containers for application development ensures that the developers have an efficient and environment-independent application whose code behavior is predictable, regardless of the operating system it runs on. Kubernetes, therefore, uses containers to package and manage an application’s code dependencies, settings, and libraries. With the rise of Kubernetes, complementary cloud services such as Amazon EKS have grown in popularity, aiming to make it easier for cloud developers to use Kubernetes.

![Amazon EKS Overview](https://sysdig.com/wp-content/uploads/amazon-eks-overview.jpg)

_Amazon EKS Overview_ (Source: Amazon)

## Amazon EKS Security

We can’t talk about the security of any AWS cloud service unless we first understand how it fits into the shared responsibility model. AWS oversees the security _of_ the cloud, while the client is responsible for the security _in_ the cloud. AWS manages the Kubernetes dashboard and control plane through EKS, which includes the ETCD database, Kubernetes clusters, and any other infrastructure service used by AWS to deliver a safe and dependable Kubernetes. Self-managed workers and EKS cluster configuration – such as IAM, pod security, [runtime security](https://sysdig.com/use-cases/cloud-threat-detection-and-response/), network security, worker node scalability, and container image components – are the responsibility of the customer.

![Amazon EKS Shared Responsibility Model](https://sysdig.com/wp-content/uploads/amazon-eks-shared-responsibility-model.jpg)

_Amazon EKS Shared Responsibility Model_ (Source: [aws.amazon.com](https://aws.amazon.com/compliance/shared-responsibility-model/))

## Amazon EKS Security Best Practices

Before developing any system, it’s critical to understand where the line between the service provider’s and the customer’s duties should be drawn. In the process, you ought to pay attention to the security implications of the system and how you handle its components in your practices. This way, you can identify the potential risks associated with malpractice incidents such as unauthorized access, breach of data confidentiality, broken authentication, system misconfiguration, and any other system fraudulent incidents. Implementing best practices during system design and development helps in setting a well-defined procedure that ensures faster response to security incidents and improves the overall organization’s security posture. The AWS EKS is highly supported by AWS to ensure that the customers and its users have the foundational tools and techniques to achieve regulatory and security compliance.

### Identity and Access Management

Identity and Access Management (IAM) is an AWS service used to manage authorization and authentication on the other AWS resources. It uses permissions and policies to assign roles to different users, which governs their privileges and actions when using various AWS resources. When working with EKS, one of the best practices for security is to follow the ‘Least Privilege Principle’ which states that a user should not be assigned more permissions than they need. This way, only the permissions required to execute a task are granted.

IAM Roles for Service Accounts (IRSA) is a feature used within the IAM to assign roles to Kubernetes service accounts. IRSA is used to create workload-specific roles within Kubernetes to ensure that the least security principle is applied at a pod and node level. It achieves this by integrating an OpenID Connect (OIDC) identity provider and Kubernetes service account annotations, to ensure the minimum privilege is assigned.

![How AWS IAM and Kubernetes Integrate to form IRSA](https://sysdig.com/wp-content/uploads/kubernetes.jpg)

_How AWS IAM and Kubernetes Integrate to form IRSA_ (Source: [AWS Blog](https://d2908q01vomqb2.cloudfront.net/ca3512f4dfa95a03169c5a670a4c91a19b3077b4/2019/08/12/irp-eks-setup-1024x1015.png))

An example of an IRSA feature in action in Kubernetes and EKS would be in applying role-based access control to differentiate cluster privileges. One key challenge faced in Kubernetes is that the pods running on the same node share the same set of permissions. This can violate the least privilege principle. To solve this challenge and grant access to the specific node, you can use IRSA to block access to the instance metadata, which prevents other pods from inheriting the role assigned to the specific worker node.

```yaml
Code: block pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-metadata-access
  namespace: example
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32
Modify security access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-metadata-access
  namespace: example
spec:
  podSelector:
    matchLabels:
      app: myapp
    policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 169.254.169.254/32
```

Generally, IAM is an important service when working with EKS to ensure holistic visibility and control over all levels of privileged access when using the resource. Other ways of ensuring that IAM meets the EKS security best practices include implementing a strong password policy to control workflow access, using multi-factor authentication (MFA), use of tokenization access keys, and session management, as well as reviewing and revoking unnecessary anonymous access to applications.

### Security Groups for Pods

In Kubernetes, a pod is a group of the smallest deployable units of computing that share storage and network resources and specify how containers are run. One of the main problems faced in containerization in Kubernetes is the lack of a common way of running applications with varied network security requirements. With pods running on shared compute resources, AWS uses AWS Security Groups for pods to control inbound and outbound network traffic within the cluster instance level. This way, security groups for pods can be used to set network security rules spanning within the pods and outside the AWS service traffic, defined in a single EC2 security instance, and applied to applications with Kubernetes native APIs. Security Groups are, therefore, attached to pods running inside the Kubernetes cluster to act as a virtual firewall for instances within the subnet in the VPC.

When implementing security groups for pods, one of the key considerations is to ensure that the container capabilities usually inherited from the root Linux host are restricted and cannot run as privileged. This is because containers do not need these privileges to function properly and could end up interfering with pod mutation. AWS also defines a pod security policy for ensuring that the pods meet the required security requirements before being created and being bound to service roles and accounts. One key way of restricting pod privilege is by setting the eks-vpc-resource-controller and vpc-resource-controller Kubernetes service accounts, defined in the Kubernetes ClusterRoleBinding for the PodSecurityPolicy assigned Role. As a best practice, service accounts are scoped within a particular namespace to bind them to privileged pods, outside which the namespaces cannot be accessed. An example of such a policy is shown below:

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
    name: restricted
    annotations:
        seccomp.security.alpha.kubernetes.io/allowedProfileNames: 'docker/default,runtime/default'
        apparmor.security.beta.kubernetes.io/allowedProfileNames: 'runtime/default'
        seccomp.security.alpha.kubernetes.io/defaultProfileName:  'runtime/default'
        apparmor.security.beta.kubernetes.io/defaultProfileName:  'runtime/default'
spec:
    privileged: false
    # Required to prevent escalations to root.
    allowPrivilegeEscalation: false
    # This is redundant with non-root + disallow privilege escalation,
    # but we can provide it for defense in depth.
    requiredDropCapabilities:
    - ALL
    # Allow core volume types.
    volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    # Assume that persistentVolumes set up by the cluster-admin are safe to use.
    - 'persistentVolumeClaim'
    hostNetwork: false
    hostIPC: false
    hostPID: false
    runAsUser:
        # Require the container to run without root privileges.
        rule: 'MustRunAsNonRoot'
    seLinux:
        # This policy assumes the nodes are using AppArmor rather than SELinux.
        rule: 'RunAsAny'
    supplementalGroups:
        rule: 'MustRunAs'
        ranges:
        # Forbid adding the root group.
        - min: 1
          max: 65535
    fsGroup:
        rule: 'MustRunAs'
        ranges:
        # Forbid adding the root group.
        - min: 1
          max: 65535
    readOnlyRootFilesystem: false
```
## Pod Security Standards

When working with security groups for pods, one needs to enforce mechanisms to set standards for pod security. There are three types of policy for Pod Security Groups:

- **Restrictions:** This policy is used to primarily target running security-critical applications that could impact the overall functionality. For example, a constraint preventing an application from running as a root or a root group.
- **Privilege Policy:** Permission-level policies, such as logging agents, storage drivers, CNIs, and other system-wide applications that require permitted access, are created using this.
- **Baseline Policy:** This is a basic set of constraints that prevent privilege escalation by preventing the usage of hostNetwork, hostPID, hostIPC, hostPath, and hostPort, as well as the inability to add Linux capabilities.

## Checklist for EKS Security

As discussed above, most of the security monitoring responsibility lies in the hands of the customer when working with the Amazon EKS. Therefore, it is important to invest in a good monitoring tool to provide end-to-end visibility into the Kubernetes cluster health and to detect any form of unauthorized activity within the pods. There are three main items in the checklist to ensure that the security metric is met:

- **Resource Metrics** – this is used to monitor the utilization of resources in comparison to the workload. It checks the usage and capacity of pods, underlying EC2 instances, and containers to ensure that different layers of your cluster, including nodes and pods running on them, can run the workload or accommodate a new workload.
- **The state of Kubernetes objects** – this checks the health status and availability of the current objects such as nodes and pods within your cluster’s control plane. The control plane allows you to have an overall picture of the performance and throughput of requests made within the clusters. This metric helps in identifying cluster-related problems brought about by API servers.
- **AWS Service Metrics** – When working with the EKS cluster, AWS will automatically provision resources to help with the overall EKS infrastructure. It is important, therefore, to monitor such services that are vital in the running of your Kubernetes containers, thus getting a full picture of the whole EKS infrastructure. Some of the AWS services used in the EKS cluster include the [Elastic Load Balancer](https://aws.amazon.com/elasticloadbalancing/) (ELB) for load balancing, [Auto Scaling](https://aws.amazon.com/autoscaling/) for dynamic scaling of worker nodes, [Elastic Compute Cloud](https://aws.amazon.com/ec2/) (EC2) for provisioning worker nodes, as well as the EBS for providing persistent storage volumes.

## Conclusion

With the rise of cloud computing uptake in digitization, it is imperative to say that observability and monitoring are some of the key best practices when using cloud services. Amazon EKS is an important tool when running Kubernetes container applications, hence the emphasis on ensuring the EKS clusters are monitored. As a user, you might be wondering where to start in monitoring your EKS clusters.

Here is a suggestion: Sysdig Monitor and Sysdig Secure. These are the components of the Sysdig Secure DevOps Platform, which are used to monitor and secure Amazon EKS using a single agent and unified platform. Sysdig assists AWS customers in shipping cloud apps quicker by allowing them to observe more, protect more, and troubleshoot deployed microservices in less time. To get started with the Sysdig DevOps Platform, follow this guide.