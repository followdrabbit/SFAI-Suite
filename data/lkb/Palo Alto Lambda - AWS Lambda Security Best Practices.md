# AWS Lambda Security Best Practices

This document from Prisma by Palo Alto Networks addresses the best security practices for serverless applications on AWS Lambda, including:

## Preface

This e-book serves as a guide to security awareness and education for organizations developing serverless applications on AWS Lambda. With many organizations still exploring the serverless architecture or taking their first steps into the serverless world, we believe this information is critical for success in building AWS Lambda-based applications that are robust, secure, and reliable.

## AWS Lambda Overview

AWS Lambda is an event-driven serverless computing platform, provided as part of Amazon Web Services (AWS). It is a computing service that runs code in response to events and automatically manages the computing resources required by that code. With AWS Lambda, organizations can run code for virtually any type of application or backend service, all with zero administration.

### AWS Lambda Benefits

- **Automated Resource Management**: Run function code without the need to provision or manage servers.
- **Automatic Scaling**: Serverless code runs in parallel, each process is triggered individually, scaling precisely with the workload size.
- **Usage-Based Billing**: Billing only applies to the compute time consumed, with no charge when code is not running.

## Serverless Security

Adopting the serverless architecture allows organizations to focus on the core product functionality, dispensing with concerns about the operating system (OS), application server, or underlying software execution environment. With serverless architecture, the responsibility for applying security patches to the OS and application servers shifts to the serverless architecture provider.

### Shared Responsibility Model in Serverless Security

- **Serverless Provider**: Responsible for the security of the data center, network, servers, operating systems, and their configurations.
- **User/Developer**: Responsible for application logic, code, data, and configurations at the application level.

## Key Security Risks in Serverless

The serverless architecture introduces a new set of security considerations, including:

- **Increased Attack Surface**: Serverless functions can consume data from a wide range of event sources, increasing the attack surface.
- **Attack Surface Complexity**: The new nature of serverless architecture can make its attack surface difficult to understand.
- **System Complexity**: Visualizing and monitoring serverless architecture is still more complex than in standard software environments.
- **Inadequate Security Testing**: Testing the security of serverless architecture is more complex, especially when applications interact with remote or cloud-based services.
- **Traditional Security (firewalls, WAFs, IPS/IDS)**: Using serverless architecture prevents the implementation of traditional security layers.

These risks highlight the importance of understanding and implementing robust security practices when working with serverless technologies, such as AWS Lambda.

## Preventing Lateral Movement in the Cloud with AWS IAM

Adopting the principle of least privilege is crucial when configuring AWS Lambda functions. This means assigning functions only the permissions strictly necessary to perform their intended logic. Poor permission management can allow vulnerabilities in one function to be exploited to access or modify resources improperly.

### Best Practices:
- Use IAM to control access granularly.
- Apply the minimum necessary permissions for each Lambda function.

## Logs and Audit Trails for AWS Lambda

The ability to record and monitor activities is fundamental to security and compliance. AWS CloudWatch and AWS CloudTrail offer powerful features for this purpose.

### AWS CloudWatch:
- Monitors execution metrics and allows investigation of abnormal activity spikes.
- Collects log data, metrics, and events to offer a unified view of AWS resources.

### AWS CloudTrail:
- Records events that may indicate unauthorized access or improper changes.
- Enables the creation of audit trails for continuous monitoring of AWS account activities.

Implementing a robust logging strategy and utilizing available auditing tools are essential steps to maintain the security of Lambda functions and other AWS resources.

## Scalability and How to Avoid DoS Attacks in AWS Lambda

One of the biggest perceived benefits of serverless architecture is automatic scalability. However, there are limitations and best practices that must be followed to ensure that serverless applications can scale safely and effectively.

### Scalability Considerations:
- **Types of Invocation**: Synchronous and Asynchronous, each with its own implications for scalability and security.
- **Retrial Mechanisms**: How to configure and the impact on user experience and application performance.
- **Concurrency Limits**: The importance of correctly configuring to prevent denial of service (DoS) and ensure availability.

## Access Control with AWS Config

AWS Config is a powerful tool for governance, compliance, and risk management. It allows recording and tracking AWS resource configurations, including Lambda functions, and assessing compliance with internal policies and external regulations.

### AWS Config Benefits for Lambda Security:
- **Continuous Monitoring**: Records configuration and code changes for Lambda functions.
- **Continuous Assessment**: Audits Lambda function configurations' compliance with organizational policies.
- **Change Management**: Tracks relationships between functions and resources, facilitating the identification of insecure or non-compliant configurations.

## API Gateway and Access Control

Amazon API Gateway plays a crucial role in securing APIs, offering traffic management, authorization and authentication, monitoring, and API version control.

### Best Practices for API Gateway Security:
- **Use of API Keys**: To control and monitor access to the APIs.
- **Usage Plans**: To define quotas and rate limits for calls, helping to prevent abuse and DoS attacks.
- **Authentication and Authorization**: Implementation of robust mechanisms, such as Amazon Cognito or Lambda authorizer functions, to validate access.

Implementing these practices and tools helps ensure that serverless applications on AWS are secure, scalable, and compliant with relevant policies and regulations.

## AWS Lambda Security with Prisma Cloud

Prisma Cloud, from Palo Alto Networks, offers a comprehensive security solution for serverless applications, including AWS Lambda. This end-to-end platform provides threat detection, governance, real-time workload visibility, and protection, as well as threat prevention.

### Key Features of Prisma Cloud:
- **Serverless Application Firewall and Runtime Protection**: Automatic defense against application-layer attacks, such as SQL injections and remote code execution.
- **Serverless Security Posture**: Integration with the CI/CD process for static scanning of serverless projects, identifying overly permissive permissions and vulnerable dependencies.
- **Serverless Visibility**: Detailed monitoring of function executions to identify and block malicious behaviors, providing forensic data for security investigations.

## Conclusion

Adopting robust security practices is crucial when developing and operating serverless applications on AWS Lambda. Organizations should leverage tools and platforms like Prisma Cloud to enhance the security, compliance, and visibility of their serverless applications. Implementing a comprehensive security architecture, including proper permission configuration, log management and audit trails, and runtime protection, is essential for protecting applications against emerging threats and ensuring compliance with applicable regulations.

By following the best security practices for AWS Lambda as outlined in this guide, organizations can develop serverless applications that are not only efficient and scalable but also secure and resilient to cyber attacks.
