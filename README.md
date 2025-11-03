# 💬 Banking Chatbot using AWS Lex, Lambda, and SES

An AI-powered *Banking Chatbot* built using *Amazon Lex V2, **AWS Lambda, **DynamoDB, **SES, and **CloudFormation*.  
It supports *OTP verification via email, **secure balance inquiry, **money transfer, **payments, and **thank you / fallback intents*.  
The project is fully deployed with *CloudFront + S3 web UI* integration.

---

## 🚀 Project Overview

This chatbot acts as a *virtual banking assistant* that can:
- 💵 Check account balance  
- 💳 Perform money transfers and payments  
- 📩 Send and verify OTPs via email (for security)  
- 👋 Greet users with a welcome message  
- 🧠 Handle fallback and thank-you responses  

Built end-to-end on *AWS Cloud* with a simple web interface for interaction.

---

## 🧠 Architecture Workflow

1. *User* interacts with the web UI hosted on *Amazon S3* (served via *CloudFront*).  
2. *Amazon Lex Bot* receives the user’s input and triggers *AWS Lambda*.  
3. *Lambda Function*:
   - Generates and sends OTP to the user’s verified email (via *Amazon SES*).  
   - Verifies OTP within 5 minutes using *DynamoDB*.  
   - Returns banking responses to Lex.  
4. *CloudFormation Template* automates deployment of all backend resources.  
5. *Lex Web UI* configuration connects the chatbot to the frontend securely.

---

## 🧩 AWS Services Used

| Service | Purpose |
|----------|----------|
| *Amazon Lex V2* | Conversational interface and NLP engine |
| *AWS Lambda* | Handles OTP generation, verification, and logic |
| *Amazon DynamoDB* | Temporary OTP storage (expires after 5 minutes) |
| *Amazon SES* | Sends OTP to verified email addresses |
| *Amazon S3* | Hosts static web UI files |
| *Amazon CloudFront* | Distributes the web UI globally (HTTPS) |
| *AWS CloudFormation* | Infrastructure as Code (deployment automation) |

---

## 🗂 Folder Structure
