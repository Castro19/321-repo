# AWS Securing Access to Cloud Resources

## IAM Fundamentals

### What is IAM?

- Identity and Access Management Service (**IAM**):
  - Helps control access to AWS resources
  - Who is authenticated and who is authorized to use your AWS Resources

### IAM Overview

- **User**: A person or app that can authenticate w/ an AWS Account

- **Group**: A collection of IAM users granted identical authorization

- **Role**: An identity used to grant a temportary set of permissions to use AWS resources

- **IAM Policy**: A document that defines the resources that can be accessed & level of access for each resource

### Requests in IAM

- A request is made every time there is an attempt to use the AWS management console, API, or AWS CLI.

- The request has the following information:

  - **Actions or Operations**: What the principal wants to perform
  - **Resources**: The object where the actions or operations are performed
  - **Principal**: The person or app that sends a request by using a user or role
  - **Environment Data**: The IP address, user agent, SSL, or time of day
  - **Resource Data**: Data related to the resource being requested.

## Using IAM for Authenticating

### IAM Roles

- Provides temporary security creds.

- Used to delegate access

1. IAM policy grant access to to the AWS resource

   - Policy is attached to the role

2. The EC2 instance **assumes** the role

3. The application has permission to access the AWS resource

### Authentication Scenario

1. The admin **creates the role** that grants permissions (read/write) to the resource

2. The admin grants permissions to the members of a dev group to **assume the role**

3. A user in the group **requests access to the role**

4. AWS STS **returns the role creds**

5. The user now has access to the resource by **using the role creds**.

## Authorizing with IAM

### Principle of Least Privilege

- Grant the minimum number or permissions that are needed for the job role

- Grant additional access as needed

- Follow this rule when granting account access

### Policies and Permissions

- Grant permissions in a policy written in JSON that define the effect, actions, and operations that an entity can make to an AWS resource

- For every request made by a principal, AWS evaluates the permissions in these policies and makes the decision whether to allow or deny the request

- Attach IAM Policies to IAM users, groups, or roles

### Managed & Inline IAM Policies

- When IAM determines permissions, an **explicit deny** will always override any allow statement.

#### Managed Policies

- Standalone identity-based policies

- Attached to multiple users, groups, and roles.

- **Features**: Reusability, central change management, ...

#### Inline Policies

- Embedded in a principal entity

- Useful for a strict 1:1 Relationship between a policy and the entity

  - Cannot be inadvertently attached to the wrong policy

## Questions

Task 1: Accessing the console as an IAM user
Do you think the kind of authentication you used to login was a good choice?  
Why or why not? Does AWS provide alternative authentication mechanisms?

- **Answer**: I don't think this authentication was a good choice because there could be security risks where a hacker that knows the AWS details could easily break in. AWS does provide MFA which would make this approach much safer.

Task 2: Attempting read-level access to AWS services
What is EC2, and why are there so many API errors displayed? What is S3, and what is contained in the buckets?

- **Answer**: EC2 provides web services in the cloud where developers can run their own computer applications. There were many API errors in EC2 because of the lack of permissions associated with the IAM user `devuser`. Following the **principle of least privilege**, permissions were not set to `devuser`, to prevent accidental modifications the attack surface area for hackers.

- **S3** is an object storage service that stores and protects data for software applications. In the buckets, there were images uploaded, however S3 buckets can hold any type of data such as PDFs, files, or documents.

Task 3: Analyzing the identity-based policy applied to the IAM user
Why can’t you see the security recommendations and IAM resources? What does the JSON in DeveloperGroupPolicy describe? Why do you think you were permitted to copy the JSON?

- I was unable to see the security recommendations and IAM resources because the role I was given did not contain the privilege for these actions. In the DeveloperGroupPolicy, it described all the permissions my role had such as read-only acces to IAM resources and S3 permissions to create new buckets and list buckets and the content of specified buckets. I believe I was able to copy the JSON because I had read access to the IAM policies.

Task 4: Attempting write-level access to AWS services
What policy permitted you to create a bucket? Why did the upload fail, and what
permission do you need so it will succeed? What were your impressions on the
listing of Actions Defined by Amazon S3, and how easy was it for you to
understand them?

Task 5: Assuming an IAM role and reviewing a resource-based policy
Why could you switch roles? Where in the U.S. is the photo in Image2.jpg taken
from? How can assuming roles encourage least privilege?

Task 6: Understanding resource-based policies
Explain how the role-based and resource-based policies interact to permit access to
different buckets for BucketsAccessRole.

Challenge task
How did you upload Image2.jpg to bucket3? Can you access other buckets? Why or why not?

- For this challenge task I tried to upload a file as devuser with no role assumed and try again with the BucketsAccessRole. In both scenarios it failed, however, I was able to view the bucket policy while I assumed the BucketsAccessRole which showed the role `OtherBucketAccessRole` that had permissions to upload an image into the S3 bucket. I was able to access other buckets based on role permissions in the bucket policies depending on which role I assumed.

Capital One Breach
Based your experience with AWS IAM during this lab, what is your hypothesis on
how errors in S3 security policies affected the Capital One breach that was
discussed in lecture? What advice would you give Capital One to fix their policies
and avoid another breach? What advice would you give AWS to improve their
IAM so their customers would not make mistakes like this again?
