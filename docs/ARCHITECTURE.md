# 🏗️ Architecture Deep Dive

## System Overview

This project implements an **AI-Driven Cloud Automation System** using the **Function Calling** pattern.

---

## 🧠 Core Concept: AI Function Calling

### What is Function Calling?

**Traditional Chatbot**:
- AI just talks
- Cannot perform actions
- User must manually execute commands

**Function Calling AI**:
- AI decides which function to call
- AI extracts parameters from natural language
- AI executes actions autonomously

### Example Flow

```
User: "Create a small VM in Southeast Asia for testing"

┌─────────────────────────────────────────────┐
│ Step 1: AI Analyzes Intent                  │
│ - Action: Create VM                         │
│ - Size: Small (B1s)                         │
│ - Region: Southeast Asia                    │
│ - Purpose: Testing                          │
└─────────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ Step 2: AI Chooses Function                 │
│ Function: create_vm                         │
│ Parameters: {                               │
│   "size": "B1s",                            │
│   "region": "southeastasia",                │
│   "name": "test-vm-001"                     │
│ }                                            │
└─────────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ Step 3: Backend Executes                    │
│ 1. Validate parameters                      │
│ 2. Check budget                             │
│ 3. Call Azure SDK                           │
│ 4. Return result                            │
└─────────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────┐
│ Step 4: AI Responds to User                 │
│ "I've created a B1s VM in Southeast Asia    │
│  named test-vm-001. It will cost ~$0.01/hr" │
└─────────────────────────────────────────────┘
```

---

## 📊 Data Flow

### 1. User → Frontend
```javascript
// User types message
"Create a VM for testing"

// React sends to backend
POST /api/chat
{
  "message": "Create a VM for testing",
  "conversation_id": "abc123"
}
```

### 2. Frontend → Backend API
```python
# FastAPI receives request
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Pass to AI Agent
    response = await ai_agent.process(request.message)
    return response
```

### 3. Backend → AI Service
```python
# Send to OpenAI/Claude with function definitions
messages = [
    {"role": "system", "content": "You are a cloud engineer assistant..."},
    {"role": "user", "content": "Create a VM for testing"}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_vm",
            "description": "Create a virtual machine in Azure",
            "parameters": {
                "type": "object",
                "properties": {
                    "size": {"type": "string", "enum": ["B1s"]},
                    "region": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["size", "region"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"  # Let AI decide
)
```

### 4. AI → Function Execution
```python
# AI returns function call
{
    "function_call": {
        "name": "create_vm",
        "arguments": {
            "size": "B1s",
            "region": "southeastasia",
            "name": "test-vm-001"
        }
    }
}

# Backend executes
if response.tool_calls:
    function_name = response.tool_calls[0].function.name
    arguments = json.loads(response.tool_calls[0].function.arguments)

    # Call actual function
    result = await execute_function(function_name, arguments)
```

### 5. Function → Azure SDK
```python
# Azure SDK execution
from azure.mgmt.compute import ComputeManagementClient

async def create_vm(size, region, name):
    # 1. Check budget first
    estimated_cost = estimate_vm_cost(size)
    current_spend = get_current_spend()

    if current_spend + estimated_cost > BUDGET_LIMIT:
        return {"status": "simulated", "message": "Budget exceeded, simulated only"}

    # 2. Create VM
    compute_client = ComputeManagementClient(credential, subscription_id)
    vm_params = {
        "location": region,
        "hardware_profile": {"vm_size": size},
        # ... other params
    }

    result = compute_client.virtual_machines.begin_create_or_update(
        resource_group,
        name,
        vm_params
    )

    return {"status": "created", "vm_name": name}
```

### 6. Result → User
```python
# Backend sends result back to AI
function_result = {
    "status": "created",
    "vm_name": "test-vm-001",
    "cost_per_hour": 0.01
}

# AI formats user-friendly response
final_response = "I've created a B1s VM named test-vm-001 in Southeast Asia.
                   It will cost approximately $0.01/hour."

# Return to frontend
return {"message": final_response}
```

---

## 🔧 Component Details

### Backend Architecture

```
backend/
├── app/
│   ├── main.py                  # FastAPI app, routes
│   ├── ai_agent.py              # AI function calling logic
│   ├── azure_functions.py       # Azure SDK wrappers
│   ├── budget_control.py        # Cost management
│   ├── config.py                # Environment config
│   └── models.py                # Pydantic models
```

#### main.py - API Server
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Azure AI Automation API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint"""
    response = await ai_agent.process(request.message)
    return response

@app.get("/api/resources")
async def list_resources():
    """List all Azure resources"""
    return await azure_functions.list_all_resources()

@app.get("/api/budget")
async def get_budget_status():
    """Get current budget usage"""
    return budget_control.get_status()
```

#### ai_agent.py - AI Decision Engine
```python
from openai import AsyncOpenAI

class AIAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.tools = self._define_tools()

    def _define_tools(self):
        """Define available functions for AI"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_vm",
                    "description": "Create a B1s virtual machine in Azure. Use for testing or small workloads.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "VM name (lowercase, alphanumeric)"
                            },
                            "region": {
                                "type": "string",
                                "enum": ["southeastasia", "eastasia"],
                                "description": "Azure region"
                            }
                        },
                        "required": ["name", "region"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "stop_vm",
                    "description": "Stop a running virtual machine to save costs",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                }
            }
        ]

    async def process(self, user_message: str):
        """Process user message and execute functions"""
        messages = [
            {
                "role": "system",
                "content": """You are an Azure cloud engineer assistant.
                Help users manage their Azure infrastructure efficiently.
                Always consider cost and best practices."""
            },
            {"role": "user", "content": user_message}
        ]

        # First AI call - decide what to do
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        # Check if AI wants to call a function
        if response.choices[0].message.tool_calls:
            # Execute the function
            tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Call actual Azure function
            result = await self._execute_function(function_name, arguments)

            # Second AI call - format result for user
            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

            final_response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages
            )

            return final_response.choices[0].message.content
        else:
            # AI just wants to talk
            return response.choices[0].message.content

    async def _execute_function(self, name: str, args: dict):
        """Execute the requested function"""
        if name == "create_vm":
            return await azure_functions.create_vm(**args)
        elif name == "stop_vm":
            return await azure_functions.stop_vm(**args)
        # ... other functions
```

#### budget_control.py - Cost Guardian
```python
class BudgetControl:
    MONTHLY_LIMIT = 10.00  # $10 max

    def __init__(self):
        self.current_spend = 0.0
        self.operations_log = []

    async def check_and_approve(self, operation: str, estimated_cost: float) -> bool:
        """Check if operation is within budget"""
        total = self.current_spend + estimated_cost

        if total > self.MONTHLY_LIMIT:
            logger.warning(f"Budget exceeded: ${total:.2f} > ${self.MONTHLY_LIMIT}")
            return False

        self.operations_log.append({
            "operation": operation,
            "estimated_cost": estimated_cost,
            "timestamp": datetime.now()
        })

        return True

    def estimate_vm_cost(self, size: str, hours: int = 730) -> float:
        """Estimate monthly VM cost"""
        hourly_rates = {
            "B1s": 0.0104,  # $0.0104/hour in Southeast Asia
        }
        return hourly_rates.get(size, 0.0) * hours

    def get_status(self) -> dict:
        """Get current budget status"""
        return {
            "limit": self.MONTHLY_LIMIT,
            "current_spend": self.current_spend,
            "remaining": self.MONTHLY_LIMIT - self.current_spend,
            "percentage_used": (self.current_spend / self.MONTHLY_LIMIT) * 100
        }
```

---

## 🎨 Frontend Architecture

### Component Hierarchy

```
App
├── ChatInterface
│   ├── MessageList
│   │   └── Message (user/ai)
│   └── InputBox
└── Dashboard
    ├── BudgetWidget
    ├── ResourceList
    └── QuickActions
```

### State Management

```javascript
// App-level state
const [messages, setMessages] = useState([]);
const [resources, setResources] = useState([]);
const [budget, setBudget] = useState(null);

// Send message to backend
const sendMessage = async (text) => {
  // Add user message to UI
  setMessages([...messages, { role: 'user', content: text }]);

  // Call API
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  });

  const data = await response.json();

  // Add AI response
  setMessages([...messages,
    { role: 'user', content: text },
    { role: 'ai', content: data.message }
  ]);

  // Refresh resources
  fetchResources();
};
```

---

## 🔒 Security Architecture

### 1. Environment-Based Secrets
```bash
# .env file (NEVER commit this)
AZURE_SUBSCRIPTION_ID=xxx
AZURE_CLIENT_ID=xxx
AZURE_CLIENT_SECRET=xxx
AZURE_TENANT_ID=xxx
OPENAI_API_KEY=xxx
```

### 2. Azure Authentication Flow
```python
from azure.identity import DefaultAzureCredential

# In production
credential = DefaultAzureCredential()

# In development
from azure.identity import ClientSecretCredential
credential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET")
)
```

### 3. Input Validation
```python
from pydantic import BaseModel, validator

class CreateVMRequest(BaseModel):
    name: str
    region: str

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[a-z0-9-]{3,15}$', v):
            raise ValueError('Invalid VM name format')
        return v

    @validator('region')
    def validate_region(cls, v):
        allowed = ['southeastasia', 'eastasia']
        if v not in allowed:
            raise ValueError(f'Region must be one of {allowed}')
        return v
```

---

## 📈 Scalability Considerations

### Current (MVP):
- Single server
- In-memory state
- Synchronous operations

### Production Improvements:
1. **Database**: Store conversation history, resource state
2. **Queue**: Use Azure Queue for long operations
3. **Caching**: Redis for resource state
4. **Logging**: Application Insights
5. **Authentication**: Azure AD
6. **RBAC**: Multi-user support

---

## 🧪 Testing Strategy

### Unit Tests
```python
# Test AI function selection
def test_ai_selects_create_vm():
    agent = AIAgent()
    result = agent.process("Create a small VM")
    assert result.function_call.name == "create_vm"

# Test budget control
def test_budget_blocks_expensive_operations():
    budget = BudgetControl()
    budget.current_spend = 9.50
    approved = budget.check_and_approve("create_vm", 1.00)
    assert approved == False
```

### Integration Tests
```python
# Test full flow
async def test_full_chat_flow():
    response = await client.post("/api/chat", json={
        "message": "Create a test VM"
    })
    assert response.status_code == 200
    assert "created" in response.json()["message"].lower()
```

---

## 📊 Monitoring & Observability

### Metrics to Track
1. **API Performance**: Response times, error rates
2. **AI Usage**: Token consumption, function call success rate
3. **Azure Resources**: Active VMs, total cost
4. **Budget**: Current spend vs limit

### Logging Structure
```python
logger.info("Function called", extra={
    "function": "create_vm",
    "parameters": {"size": "B1s", "region": "southeastasia"},
    "user_id": "user123",
    "estimated_cost": 0.01
})
```

---

## 🎯 Design Decisions & Trade-offs

### 1. Why FastAPI?
- ✅ Async support (crucial for AI API calls)
- ✅ Automatic API documentation
- ✅ Pydantic validation
- ✅ Modern Python standards

### 2. Why Function Calling over RAG?
- ✅ Deterministic actions (RAG is for information)
- ✅ Structured outputs
- ✅ Better for automation

### 3. Why Mock Mode First?
- ✅ Test logic without Azure costs
- ✅ Develop faster
- ✅ Demo without credentials

---

## 🚀 Deployment Options

### Development
```bash
# Local
uvicorn app.main:app --reload
```

### Production
```bash
# Option 1: Azure App Service
az webapp up --name azure-ai-automation

# Option 2: Docker + Azure Container Apps
docker build -t azure-ai-automation .
az containerapp up --name azure-ai-automation
```

---

This architecture demonstrates production-ready cloud engineering practices while remaining cost-effective for a portfolio project.
