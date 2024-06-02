# Authorization and Authentication

## Introduction

### Hook

- Security in web applications is forgotten in most small web applications. In my project I will build a basic web application and implement security mechanisms with the goal to prevent malicious attacks.

### Research Question:

- How can web applications using modern web frameworks (React) ensure best practices to effectively secure user data while also providing access control?
- What are ways to prevent attacks from occurring on my web application?

### Thesis

- As someone who has built many web applications, I have always pushed security to the side. However, in this project, my goal is to build an application with security as the number one priority.
  -This includes defining roles for access control, setting up authentication using best practices, and doing penetration testing to document what features have vulnerabilities.

### Features of my Project

- **What I have built**: A fully functional web application where users can login and save **Secrets** they created using an input form.
- Users can then grant permissions to other users such as `read`, `write`, `update` and `delete`.

- **Technologies:**
  - **Front-end**: React, Typescript, JWT
  - **Back-end**: Node JS, Express, Bcrypt
  - **Databases**: MongoDB

1. Currently using `bcrypt` for password hashing and JSON Web Tokens (`JWT`) for session management
2. Role Based Access Control (`RBAC`) to enhance **Confidentiality**, **Integrity**, and **Accessibility** (`CIA`) in web applications.

- I will also try to finish one or more of the following:

1. **Penetration Testing**: Identify and exploit vulnerabilities in this web application before it can be exploited.
2. **Perform XSS**: Try to create malicious scripts that are injected inside input fields across my application.
3. **Analyze differences in HTTP and HTTPS**: Demonstrate the security enhancements HTTPS provides over HTTP, in protecting data that is being transmitted.
   - Use **Wireshark** to try and intercept the login packages to find the user's logged in username and password.

## Body Paragraphs

### Context and History of Authorization and Access Control in Web Applications

- **Authentication** and **authorization** are fundamental to making sure web applications stay secure and preventing attacks.
- Granting **Access control** using the `principle of least privilege` is essential in making sure users have the correct permissions while preventing attacks.
- **History**:
  - **Session Management (Late 1990s)**: Cookies and session IDs for improved tracking.
  - **Web Frameworks (2000s)**: Built-in authentication/authorization tools.
  - **Single Sign-On (SSO) (Mid-2000s)**: Convenient, secure access to multiple apps (e.g., SAML, OAuth).
  - **JSON Web Tokens (JWT) (Late 2000s)**: Secure transmission of auth info, stateless authentication.
  - **Fine-Grained Access Control (2010s)**: Flexible models (e.g., RBAC, ABAC).
  - **Cloud IAM (2010s-Present)**: Centralized authentication for cloud apps/resources.

### Existing Arguments

#### Security vs. Usability

- Arguments can be made that increasing security in small applications can increase the complexity of the application making it be less usable.
  - Such as creating Multi-Factor Authentication (`MFA`) or constantly requestiong permissions for access control can make users less likely to use the resource tool

#### Cost of Implementation

- Another argument can be made on how much it will cost to get these security features working.
  - This is very common for small start ups that just want to get a working product in the market.
- Arguments on whether these security features are worth the **time** and **money** being spent.

### Your Argument

#### Balancing Security with Usability

- **Enhanced Security with Bcrypt and JWT:** Implementing bcrypt allows our application to securily store user credentials by hashing passwords `with salt` in a way that even if data is compromised, the actual passwords remain protected.
- JSON Web Tokens enhance security by ensuring that user sessions are stateless and securely validated on each request.
  - In the current application these JSON web tokens expire after 1 hour but can be increased

#### Cost-Effective Security Solutions

- By implementing an open-source solution like bcrypt and JWT our application does not have to worry about out sourcing to big tech companies to handle our apps authentication.
  - User credentials (username and hashed password) can be easily stored in a MongoDB database for free!
- Implementing these security features and spending additional time making sure these features are implemented securely will save money in the long term for small companies to prevent any attacks that could expose user information resulting in law suits.

## Conclusion

- As a current Computer Science student who enjoys building web applications, I beleive that web security is a vital peice in creating software that has the potential to make or break a growing company.
- In this project, I plan on diving deep into how security in web applications work and how I can learn best practices to ensure that future web applications I work on are secure and reliable.

### Summary of Main Points

- **Authorization**: Combining Bcrypt for hashing passwords with salt and JSON Web Tokens for session management, we can authorize users into our web application.
- **Role-Based Access Control**: Providing Access control based on different roles allows for an easy to use system where users can be **admin**, **editor**, **viewer**, or not have a role at all.
- **Penetration Testing**: Finding vulnerabilities in the code and documenting them to ensure that I do not make the same mistake again.

#### Answer: Why Does This Research Matter?

- This research is important to showcase best practices when building a secure web application no matter the scale.
- From small to large projects, all web applications should ensure that user data is safe from attacks.
