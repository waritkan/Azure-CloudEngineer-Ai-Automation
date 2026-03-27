# 🚀 Quick Start Guide

Get your AI-powered Azure automation dashboard running in **5 minutes**!

---

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key (for AI features)
- Azure account (optional - can use mock mode first)

---

## ⚡ Quick Setup (Mock Mode - No Azure Needed!)

### Step 1: Clone/Download the Project

```bash
cd E:\Cloud_Engineer_Project\azure-ai-automation
```

### Step 2: Setup Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example env file
copy .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
# ENABLE_MOCK_MODE=true  (keep this as true!)
```

**Get OpenAI API Key**:
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste into `.env` file

### Step 4: Start Backend Server

```bash
# From backend folder
uvicorn app.main:app --reload
```

You should see:
```
🚀 Starting Azure AI Automation v1.0.0
📊 Mode: MOCK
✅ Application started successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Open Frontend

```bash
# From root folder
cd frontend/simple-html

# Open index.html in your browser
# Or use Python's built-in server:
python -m http.server 3000
```

Open browser to: `http://localhost:3000`

---

## 🎮 Try It Out!

Type these messages in the chat:

1. **"Create a small VM for testing"**
   - Watch AI create a simulated VM
   - See budget update
   - Notice VM appears in resources list

2. **"What VMs do I have?"**
   - AI lists all resources

3. **"What's my budget status?"**
   - AI shows spending info

4. **"Stop the test VM"**
   - AI stops the VM

---

## 🧪 Testing the API

### Using Browser
Open: http://localhost:8000/docs

You'll see interactive API documentation!

### Using curl

```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a VM for testing"}'

# List resources
curl "http://localhost:8000/api/resources"

# Check budget
curl "http://localhost:8000/api/budget"
```

---

## 🎯 Understanding Mock Mode

**Mock Mode** = Simulation only (no real Azure resources)

| Feature | Mock Mode | Azure Mode |
|---------|-----------|------------|
| AI Chat | ✅ Yes | ✅ Yes |
| Create VM | ✅ Simulated | ✅ Real |
| Budget Tracking | ✅ Yes | ✅ Yes |
| Cost | $0 Azure | Real Azure costs |
| Speed | Fast | Slower (real API) |

**Why start with mock mode?**
- ✅ Test everything without costs
- ✅ Develop safely
- ✅ Demo to others
- ✅ Learn the system

---

## 🔄 Moving to Azure Mode (Real Resources)

### Prerequisites
1. Azure account with active subscription
2. Create a Service Principal (App Registration)

### Step 1: Create Azure Service Principal

```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create service principal
az ad sp create-for-rbac --name "azure-ai-automation" --role Contributor

# Output will look like:
{
  "appId": "xxx",           # = AZURE_CLIENT_ID
  "password": "xxx",        # = AZURE_CLIENT_SECRET
  "tenant": "xxx"           # = AZURE_TENANT_ID
}

# Get subscription ID
az account show --query id -o tsv  # = AZURE_SUBSCRIPTION_ID
```

### Step 2: Create Resource Group

```bash
az group create --name rg-ai-automation --location southeastasia
```

### Step 3: Update .env

```bash
# Add to .env:
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id

# Change mode:
ENABLE_MOCK_MODE=false
```

### Step 4: Restart Backend

```bash
# Stop current server (Ctrl+C)
# Start again
uvicorn app.main:app --reload
```

You should now see:
```
📊 Mode: AZURE
```

### Step 5: Test with Real Azure

```bash
# Create real VM
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a small VM for testing"}'

# This will now create a REAL Azure VM!
# Check in Azure Portal: portal.azure.com
```

---

## 💰 Cost Management

### Expected Costs (Azure Mode)

| Resource | Cost | Notes |
|----------|------|-------|
| B1s VM (running 24/7) | ~$7.59/month | Cheapest VM |
| B1s VM (8 hours/day) | ~$2.53/month | Recommended for testing |
| OpenAI API (100 requests) | ~$0.20 | GPT-4 Turbo |
| **Total (conservative)** | **~$3/month** | Well under $10 limit |

### Cost Saving Tips

1. **Stop VMs when not in use**
   ```
   Chat: "Stop all VMs"
   ```

2. **Delete test resources**
   ```bash
   # Delete resource group when done
   az group delete --name rg-ai-automation
   ```

3. **Use Azure Free Tier**
   - First month: $200 credit
   - 12 months: Some services free

4. **Set Azure Budgets**
   ```bash
   # Set budget alert in Azure Portal
   - Go to Cost Management + Billing
   - Create Budget
   - Set limit to $10
   - Add email alert
   ```

---

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

**Error**: `openai.OpenAIError: Invalid API key`
```bash
# Check .env file has correct key
# Make sure no spaces around =
OPENAI_API_KEY=sk-your-key-here
```

### AI not responding

**Check**:
1. Is `OPENAI_API_KEY` set in `.env`?
2. Is the API key valid?
3. Do you have OpenAI credits?

**Fallback**: Use API endpoints directly without AI:
```bash
# Direct VM creation (no AI)
curl -X POST "http://localhost:8000/api/vm/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-vm-001",
    "size": "B1s",
    "region": "southeastasia"
  }'
```

### Frontend can't connect

**Error**: CORS errors in browser console

**Fix**:
- Make sure backend is running on port 8000
- Check URL in frontend is `http://localhost:8000`
- Clear browser cache

### Azure Mode issues

**Error**: `Azure credentials not configured`

**Fix**:
1. Check all `AZURE_*` variables are in `.env`
2. Verify Service Principal has Contributor role
3. Ensure Resource Group exists

**Error**: `Insufficient permissions`

**Fix**:
```bash
# Give Service Principal correct role
az role assignment create \
  --assignee <client-id> \
  --role Contributor \
  --scope /subscriptions/<subscription-id>
```

---

## 📚 Next Steps

### Learning Path

1. **Understand the Code**
   - Read [ARCHITECTURE.md](ARCHITECTURE.md)
   - Study `ai_agent.py` (how AI decides)
   - Explore `azure_functions.py` (Azure integration)

2. **Prepare for Interviews**
   - Read [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md)
   - Practice the demo
   - Understand each component

3. **Extend the Project**
   - Add more VM sizes
   - Implement VM templates
   - Add cost alerting
   - Create dashboard charts

### Useful Resources

- [Azure SDK Documentation](https://docs.microsoft.com/en-us/python/api/overview/azure/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

---

## 🎓 Understanding the Flow

```
User types: "Create a small VM"
       ↓
Frontend sends to: POST /api/chat
       ↓
Backend receives message
       ↓
AI Agent analyzes intent
       ↓
AI decides: call create_vm()
       ↓
Budget Controller checks cost
       ↓
If approved → Azure Function executes
       ↓
VM created (mock or real)
       ↓
Result returned to AI
       ↓
AI formats response
       ↓
Response sent to frontend
       ↓
User sees: "✅ VM created successfully!"
```

---

## ✅ Checklist

Before demo/interview:

- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Can send chat messages
- [ ] AI responds correctly
- [ ] Budget widget updates
- [ ] Resources list shows VMs
- [ ] Understand the code flow
- [ ] Can explain architecture
- [ ] Tested in both mock and Azure mode (if applicable)

---

## 🚀 You're Ready!

You now have a working AI-powered Azure automation dashboard!

- ✅ Runs in safe mock mode
- ✅ AI understands natural language
- ✅ Budget-aware operations
- ✅ Professional API design
- ✅ Portfolio-ready project

**Next**: Study [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) to ace your interviews! 🎯
