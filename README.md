# 🤖 AI-Powered Cloud Automation Dashboard (Azure)

> **Portfolio Project**: Demonstrate advanced Cloud Engineering skills with AI integration

[![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)

---

## 📌 Overview

Web Dashboard ที่ใช้ **AI เป็นสมอง** ในการควบคุม Azure infrastructure ผ่าน Natural Language

### ✨ Key Features

- 💬 **Chat with AI** - คุยกับ AI เหมือนคุยกับ Cloud Engineer
- 🧠 **Smart Decision Making** - AI ตัดสินใจเรียก Azure function เองโดยอัตโนมัติ
- 💰 **Budget Control** - ควบคุมค่าใช้จ่าย ไม่เกิน $10/เดือน
- 🔒 **Security First** - ไม่มี hardcoded secrets, ใช้ Azure Managed Identity
- 📊 **Cost Estimation** - ประเมินค่าใช้จ่ายก่อนสร้าง resource

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│          React Chat UI (Port 3000)                       │
└───────────────────────┬──────────────────────────────────┘
                        │ HTTP/REST API
                        ▼
┌──────────────────────────────────────────────────────────┐
│                  BACKEND API SERVER                      │
│              FastAPI (Port 8000)                         │
│                                                           │
│  ┌─────────────────────────────────────────────┐        │
│  │          AI AGENT (Function Calling)        │        │
│  │  - Analyze user intent                      │        │
│  │  - Choose appropriate function              │        │
│  │  - Execute with parameters                  │        │
│  └─────────────────────────────────────────────┘        │
│                        │                                  │
│  ┌─────────────────────┴──────────────────────┐         │
│  │                                             │         │
│  ▼                                             ▼         │
│ ┌──────────────────┐              ┌──────────────────┐  │
│ │  Budget Control  │              │  Azure Functions │  │
│ │  - Check limit   │              │  - create_vm()   │  │
│ │  - Estimate cost │              │  - stop_vm()     │  │
│ │  - Block if over │              │  - list_all()    │  │
│ └──────────────────┘              └──────────────────┘  │
│                                             │            │
└─────────────────────────────────────────────┼────────────┘
                                              ▼
                                    ┌──────────────────┐
                                    │   Azure Cloud    │
                                    │  - Virtual       │
                                    │    Machines      │
                                    │  - Cost Mgmt     │
                                    └──────────────────┘
```

