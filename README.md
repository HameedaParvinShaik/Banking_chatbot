# Banking_chatbot
# 💬 AWS Banking Chatbot with OTP Verification

This project is a *Banking Chatbot* built using *Amazon Lex, **Lambda, **SES, **DynamoDB, **S3, and **CloudFormation*.  
It includes intents like *Check Balance, **Transfer, **Payment, **Welcome, **Fallback, and **Thank You*,  
and features *OTP verification via Amazon SES* for secure access.

---

## 🧩 Workflow
1. User interacts with *Lex chatbot* (CloudFront-hosted UI).  
2. Lex triggers the *Lambda function* to process user intents.  
3. For secure actions, *SES sends OTP* to the verified email address.  
4. OTPs are stored in *DynamoDB* for 5 minutes.  
5. Lambda verifies the OTP → responds to Lex.  
6. All AWS resources are deployed automatically through *CloudFormation*.

---

## 🛠 AWS Services Used
- *Amazon Lex* – Chatbot
- *AWS Lambda* – Backend logic
- *Amazon SES* – OTP email service
- *Amazon DynamoDB* – OTP storage
- *Amazon S3* – Static site & Lambda storage
- *Amazon CloudFront* – Web UI hosting
- *AWS CloudFormation* – Deployment automation

---
