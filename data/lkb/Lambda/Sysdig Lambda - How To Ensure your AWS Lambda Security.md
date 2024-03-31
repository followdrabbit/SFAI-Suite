# How To Ensure your AWS Lambda Security

![Securing AWS Lambda](https://sysdig.com/wp-content/uploads/image1-1-1170x780.jpg)

_Source:_ [_pixabay.com_](https://pixabay.com/illustrations/hacker-hacking-cyber-security-hack-1944688/)

AWS Lambda functions provide an alternative approach for rapidly developing and deploying your applications in the cloud. When you build your applications with Lambda functions, you delegate much of the work around infrastructure provisioning and management to the cloud provider, Amazon Web Services. While that delegation removes some of the concerns around AWS Lambda security, it doesn’t eliminate them.

This article will discuss potential vulnerabilities related to AWS Lambda that you should keep in mind when using a serverless approach. We’ll explain how to secure your Lambda-based applications and also introduce other AWS Lambda security best practices that will enable you to take full advantage of this offering from AWS.

## **What is a Lambda Function?**

AWS Lambda allows you to create a function that takes input as a web request or event from an AWS resource, such as a DynamoDB event or SQS message. Lambda can process the event, including actions such as writing data to a database; then, output from the function is returned. The **benefit of using Lambda is** that **you don’t have to worry about provisioning the underlying infrastructure** or **scaling the function to handle an increased load**.

For example, you might use a Lambda function in scenarios like the following:

- **After adding a new image file to an [S3 bucket](https://sysdig.com/learn-cloud-native/cloud-security/how-does-amazon-s3-security-work/)**. This event can trigger a Lambda function to generate a thumbnail image and save it to another bucket.
- **When an HTTP request is submitted to add a new user record** to a database. Different functions could update and delete records.
- **For an interactive website that can handle authentication** and serve up web pages using calls to a Lambda function.

In addition to automatic scaling and removing the need to provision the underlying infrastructure, there are other advantages to using AWS Lambda. Compute time for Lambda is calculated at subsecond usage, meaning that you only pay for your function’s compute time. Even after the free tier expires on your account, you still get the first million requests free. Then, you only pay **$0.20** for every million requests after that.

AWS Lambda isn’t without its limitations, however. Lambda functions can only execute for a maximum of 15 minutes. The account default for Lambda execution is limited to 1,000 concurrent executions, although you can increase this limit by working with AWS support. Lambda functions may also encounter a cold-start delay, although this can be reduced based on the language used to write the Lambda function.

Depending on your use case and how you implement Lambda functions as part of your architecture, they can be a cost-effective solution to your cloud-based needs. With that said, it’s essential that you implement your Lambda solution in a secure manner and also factor in the cost of other services that you may need to support your Lambda functions.

Before continuing, remember that pricing and limitations can change over time, if you want more precise information about these depending on your case, you can dig in more in the [official AWS page](https://aws.amazon.com/es/lambda/pricing/). Now, we can go one step further, that is, AWS Lambda security and its requirements.

### **Does Lambda need to be secured?**

Using AWS Lambda does shift some aspects of the shared responsibility model to Amazon; however, there are still aspects for which you, as the owner of the Lambda implementation, are responsible. Let’s begin by exploring how the [shared responsibility model](https://sysdig.com/learn-cloud-native/cloud-security/cloud-security-posture-management/#cspm-and-shared-responsibility) applies to AWS Lambda security. Then we’ll discuss your responsibilities around security and compliance, as well as some best practices to keep your infrastructure safe from malicious actors, accidental exposure, and excessive costs.

### **Understanding the Shared responsibility security model**

The shared responsibility model outlines who is responsible for maintaining and securing different parts of the cloud infrastructure. When you use AWS virtual services (like EC2), much of the responsibility for securing and maintaining the instances lies with the consumer; however, AWS assumes additional responsibilities with AWS Lambda.

As a user of AWS Lambda, you are responsible for the following:

- Function code and any dependencies and libraries used.
- The configuration of resources.
- Identity and Access Management (IAM).

AWS is responsible for maintaining and securing the following:

- Compute resources.
- The execution environment.
- Runtime languages.
- Networking infrastructure.
- Server software.
- Underlying hardware.

If you understand these responsibilities and how they might leave you vulnerable, you’ll be better prepared to secure your Lambda implementations.

## **AWS Lambda vulnerabilities**

Although Lambdas consist of small and well-defined pieces of code, they are still coded, and therefore need the same attention as application code that’s executed in other environments. Ensure that your code is thoroughly tested and scanned to eliminate bugs or other problems that your developers might introduce through human error or inexperience.

In addition, your Lambda code might include libraries and other dependencies. Using external libraries reduces coding time and can mean you have well-tested and vetted code in your application. Still, just because everyone uses the same libraries doesn’t mean they’re secure – and you should never assume that they are. Including dependency checks as part of your development practices and deployment, pipelines is critical to protecting your Lambda functions.

As we demonstrated in [AWS Lambda Threat](https://sysdig.com/blog/exploit-mitigate-aws-lambdas-mitre/), attackers could take advantage of this misconfigured AWS Lambda function and take full control of the AWS account.

Lambda functions are essentially just mini-applications. As with other applications, you need to ensure that they are accessible only to authorized users and that you subject any input to vigorous scrutiny before processing. You also want to ensure that your Lambda is not the target of a [DDoS attack](https://sysdig.com/learn-cloud-native/cloud-security/what-is-a-dos-attack/), especially given the highly scalable nature of the environment and the need to serve legitimate consumers.

## **AWS Lambda security best practices**

Now that you understand how your Lambda functions might be vulnerable, let’s talk about some best practices you can follow to protect against these vulnerabilities when deploying and configuring your functions.

### **Identity and Access Management (IAM)**

When you deploy your Lambda function, you assign an [IAM role](https://aws.amazon.com/iam/) that defines how and where users of the Lambda function can access it. The role also determines the resources that the Lambda function can access. In alignment with IAM best practices for other resources, you’ll want to ensure that the role associated with your Lambda allows only the minimum required access allocated to ensure it can do its job. You should ensure that the role does not include unrestricted access permissions, such as those specified by a **_resource.\*_**.

### **Single Responsibility Principle**

**Your Lambda function should be tasked with performing one action and only one action**. This single responsibility principle improves the simplicity of your Lambda function, reduces the chance of introducing errors, and reduces the blast radius should it be compromised.

### **HTTP Access**

If your intention is for your Lambda to be invoked through a web request, **it’s best to route these requests through [AWS API Gateway](https://aws.amazon.com/api-gateway/)**. API Gateway provides several safeguards, including protection from DDoS attacks and other malicious attacks from bad actors in the dark recesses of the web.

### **Cleaning Up**

As a general rule, Lambda functions don’t write to the local disk. An exception to this rule is a **_/tmp_** folder to which they can write temporary data. Unfortunately, there is no guarantee that this folder’s contents will be destroyed when an invocation completes. Hence, a good best practice is to ensure that you intentionally delete everything written to this folder before the Lambda execution phase completes.

### **Scrutinize Input**

This best practice applies to all applications, but it’s worth mentioning so that it isn’t overlooked while you’re reducing complexity when moving to Lambda functions. Your **Lambda function should consider all input potentially harmful until it has been adequately validated and cleansed**. If the incoming payload doesn’t conform to expected standards, it should not be processed, and the Lambda should log the attempt for analysis by your DevOps engineers.

### **Deploy Your Lambda Functions into a VPC with Limited Permissions**

As with other cloud resources, setting up a [Virtual Private Cloud (VPC)](https://aws.amazon.com/vpc/getting-started/) that you configure with the least amount of privileges required for your Lambda functions to operate effectively is a best practice. As with the other best practices listed above, this further reduces the opportunity for an attack to use your Lambda function to access additional resources within your account.

### **Design and Implement an Effective Monitoring Plan**

Your DevOps engineers should be able to view statistics relating to your Lambda in a dashboard. You can use those provided by [CloudWatch](https://aws.amazon.com/cloudwatch/), or you can use a third-party solution that displays metrics and provides insights into invocations of the Lambda and the execution time. The dashboard should also visualize the memory and compute resources consumed, and you should set up alerts to inform your operations team when exceptions to baseline thresholds occur.

### **Maintaining Compliance**

In addition to ensuring that your Lambda functions are secure against possible attacks and misconfiguration errors, **you may also be subject to compliance requirements** if you are handling personal, medical, payment, or other sensitive data within your system. As a user of AWS Lambda, validating and ensuring compliance falls under your responsibility. To aid in this, AWS maintains [compliance programs](https://aws.amazon.com/compliance/programs/) for many common frameworks that you can use to ensure that your applications comply with applicable laws.

## **Continuing your AWS Lambda security journey**

We’ve discussed a lot of potential vulnerabilities related to AWS Lambda and several best practices that you can implement to ensure your AWS Lambda implementations are protected and safe to use. The reality is that AWS Lambda can make your application development processes more straightforward to maintain. It is imperative, however, that in simplifying and breaking applications down into individual functions, we don’t lose sight of tried-and-true development best practices. In addition, we should always start development with a security-first mindset.