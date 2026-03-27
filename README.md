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

---

## 🎯 Technical Highlights (for Interview)

### 1. **AI-Driven Function Calling**
```python
# AI analyzes: "Create a small VM in Southeast Asia"
# AI decides to call: create_vm(size="B1s", region="Southeast Asia")
# No hardcoded if/else logic needed!
```

**Why this matters**:
- Modern cloud automation uses AI for intent recognition
- Similar to Azure OpenAI Service + Function Calling
- Demonstrates understanding of LLM integration

---

### 2. **Budget-Aware Architecture**
```python
# Before creating resources:
1. Estimate cost
2. Check current spend
3. If safe → proceed
4. If over → simulate or deny
```

**Why this matters**:
- Production systems need cost controls
- Shows financial responsibility
- Real-world cloud engineering skill

---

### 3. **Security Best Practices**
```bash
# ❌ NEVER do this
AZURE_CLIENT_SECRET = "abc123..."

# ✅ Always do this
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
```

**Why this matters**:
- Prevents credential leaks
- Follows Azure Well-Architected Framework
- Production-ready security

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Azure account (Free tier OK)

### Phase 1: Basic Setup (No Azure needed)
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start
```

### Phase 2: Azure Integration
```bash
# Set environment variables
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
export OPENAI_API_KEY="your-openai-key"
```

---

## 📁 Project Structure

```
azure-ai-automation/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── ai_agent.py             # AI function calling logic
│   │   ├── azure_functions.py      # Azure SDK integration
│   │   ├── budget_control.py       # Cost management
│   │   └── config.py               # Environment config
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   ├── ChatInterface.js        # Chat UI
│   │   └── Dashboard.js            # Resource dashboard
│   ├── package.json
│   └── public/
├── docs/
│   ├── ARCHITECTURE.md             # Detailed architecture
│   ├── INTERVIEW_GUIDE.md          # How to explain this project
│   └── DEMO_SCRIPT.md              # Demo walkthrough
└── README.md
```

---

## 💡 How AI Function Calling Works

### Traditional Approach (Hard to maintain):
```python
if "create vm" in user_message:
    create_vm()
elif "stop vm" in user_message:
    stop_vm()
# ❌ Fragile, doesn't handle variations
```

### AI Function Calling (Smart):
```python
# Define available functions
tools = [
    {
        "name": "create_vm",
        "description": "Create a virtual machine in Azure",
        "parameters": {
            "size": "VM size (e.g., B1s)",
            "region": "Azure region"
        }
    }
]

# AI analyzes user intent and calls the right function
response = ai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": user_message}],
    tools=tools
)

# AI returns: function_call = "create_vm" with parameters
# ✅ Handles natural language variations automatically
```

---

## 🎤 Interview Talking Points

### "Tell me about this project"

> "I built an AI-powered cloud automation dashboard that uses GPT-4's function calling to control Azure infrastructure through natural language. Users can chat with the system like talking to a cloud engineer, and the AI automatically decides which Azure operations to perform.
>
> The system includes budget controls to prevent overspending, uses Azure SDK for resource management, and follows security best practices like environment-based credential management.
>
> I designed it with a FastAPI backend and React frontend, implementing RESTful APIs and real-time chat functionality."

### "What challenges did you face?"

> "One key challenge was implementing budget control to ensure the demo doesn't exceed the free tier. I solved this by:
> 1. Creating a cost estimation function before any operation
> 2. Tracking current spend using Azure Cost Management API
> 3. Using mock responses when budget is exceeded
>
> Another challenge was making the AI reliably choose the right functions. I solved this by providing detailed function descriptions and examples in the system prompt."

### "How would you scale this?"

> "For production:
> 1. Add authentication (Azure AD)
> 2. Implement queueing for long-running operations
> 3. Add comprehensive logging and monitoring
> 4. Use Azure Functions for serverless backend
> 5. Implement RBAC for multi-user support"

---

## 📊 Cost Breakdown

| Component | Monthly Cost |
|-----------|--------------|
| Azure B1s VM (1 hour/day) | ~$0.50 |
| OpenAI API (100 requests) | ~$0.20 |
| Azure Storage (minimal) | ~$0.10 |
| **Total** | **< $1.00** |

*Using free tiers and mock mode for most operations*

---

## 🔐 Security Features

- ✅ Environment-based secrets management
- ✅ No hardcoded credentials
- ✅ Input validation and sanitization
- ✅ Budget limits to prevent runaway costs
- ✅ Azure RBAC integration ready

---

## 📚 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Azure SDK** - Azure resource management
- **OpenAI API** - AI function calling
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Axios** - HTTP client
- **Tailwind CSS** - Styling

### Cloud
- **Azure Virtual Machines** - Compute resources
- **Azure Cost Management** - Budget tracking
- **Azure Identity** - Authentication

---

## 🎓 Learning Outcomes

By completing this project, you'll understand:

1. ✅ AI function calling and LLM integration
2. ✅ Azure SDK and resource management
3. ✅ Cloud cost optimization
4. ✅ REST API design with FastAPI
5. ✅ Modern frontend development with React
6. ✅ Security best practices in cloud applications
7. ✅ Production-ready application architecture

---

## 📖 Additional Resources

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Detailed system design
- [docs/INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md) - Interview preparation
- [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) - Step-by-step demo

---

## 📄 License

MIT License - Feel free to use this for your portfolio!

---

## 👤 Author

Created as a portfolio project to demonstrate Cloud Engineering expertise with AI integration.

**Key Skills Demonstrated**:
- Azure Cloud Architecture
- AI/ML Integration
- Python Backend Development
- Modern Web Development
- DevOps Best Practices
- Cost Optimization
- Security Implementation

---

## 🙏 Acknowledgments

Built with inspiration from:
- Azure OpenAI Service architecture
- Model Context Protocol (MCP) concepts
- Modern cloud-native design patterns

---

**Ready to impress in your next Cloud Engineer interview!** 🚀
