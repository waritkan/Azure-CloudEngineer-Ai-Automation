"""
FastAPI Application - Main Entry Point

This is the API server that:
1. Receives requests from frontend
2. Routes to AI Agent
3. Returns responses

Endpoints:
- POST /api/chat - Chat with AI
- GET /api/resources - List all resources
- GET /api/budget - Get budget status
- POST /api/vm/create - Create VM directly
- POST /api/vm/{name}/stop - Stop VM
- POST /api/vm/{name}/start - Start VM
- DELETE /api/vm/{name} - Delete VM
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings, get_mode
from app.models import (
    ChatRequest,
    ChatResponse,
    CreateVMRequest,
    VMCreateResponse,
    ResourceListResponse,
    BudgetStatus,
    VMActionRequest
)
from app.ai_agent import get_ai_agent
from app.azure_functions import get_resource_manager
from app.budget_control import get_budget_controller

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"📊 Mode: {get_mode().upper()}")

    # Initialize global instances (already done via imports)
    ai_agent = get_ai_agent()
    resource_manager = get_resource_manager()
    budget = get_budget_controller()

    logger.info("✅ Application started successfully")

    yield

    # Shutdown
    logger.info("👋 Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Azure Cloud Automation Dashboard",
    lifespan=lifespan
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Health & Info ====================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "mode": get_mode(),
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "resources": "/api/resources",
            "budget": "/api/budget",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    ai_agent = get_ai_agent()
    return {
        "status": "healthy",
        "mode": get_mode(),
        "ai_enabled": ai_agent.ai_enabled,
        "budget_limit": settings.MONTHLY_BUDGET_LIMIT
    }


# ==================== AI Chat Endpoint ====================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - talk to AI

    The AI will:
    1. Understand your intent
    2. Decide which function to call (if any)
    3. Execute the function
    4. Return a formatted response

    Example requests:
    - "Create a small VM for testing"
    - "List all my VMs"
    - "What's my budget status?"
    - "Stop the test VM"
    """
    try:
        ai_agent = get_ai_agent()
        response = await ai_agent.process(
            user_message=request.message,
            conversation_id=request.conversation_id or "default"
        )
        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Resource Management ====================

@app.get("/api/resources", response_model=ResourceListResponse)
async def list_resources():
    """
    List all virtual machines

    Returns:
    - List of all VMs
    - Total count
    - Total monthly cost
    """
    try:
        resource_manager = get_resource_manager()
        resources = await resource_manager.list_all_resources()
        return resources

    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/vm/create", response_model=VMCreateResponse)
async def create_vm(request: CreateVMRequest):
    """
    Create a virtual machine directly (without AI)

    Use this if you want to bypass the AI and create a VM directly.
    The AI chat endpoint is recommended for better UX.
    """
    try:
        resource_manager = get_resource_manager()
        result = await resource_manager.create_vm(
            name=request.name,
            region=request.region,
            size=request.size
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating VM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/vm/{vm_name}/stop")
async def stop_vm(vm_name: str):
    """Stop (deallocate) a VM to save costs"""
    try:
        resource_manager = get_resource_manager()
        result = await resource_manager.stop_vm(vm_name)
        return result

    except Exception as e:
        logger.error(f"Error stopping VM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/vm/{vm_name}/start")
async def start_vm(vm_name: str):
    """Start a stopped VM"""
    try:
        resource_manager = get_resource_manager()
        result = await resource_manager.start_vm(vm_name)
        return result

    except Exception as e:
        logger.error(f"Error starting VM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/vm/{vm_name}")
async def delete_vm(vm_name: str):
    """Delete a VM permanently"""
    try:
        resource_manager = get_resource_manager()
        result = await resource_manager.delete_vm(vm_name)
        return result

    except Exception as e:
        logger.error(f"Error deleting VM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Budget Management ====================

@app.get("/api/budget", response_model=BudgetStatus)
async def get_budget():
    """
    Get current budget status

    Returns:
    - Budget limit
    - Current spend
    - Remaining budget
    - Percentage used
    """
    try:
        budget = get_budget_controller()
        return budget.get_status()

    except Exception as e:
        logger.error(f"Error getting budget: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/budget/history")
async def get_budget_history(limit: int = 10):
    """Get recent operations history"""
    try:
        budget = get_budget_controller()
        return {
            "operations": budget.get_operations_history(limit=limit)
        }

    except Exception as e:
        logger.error(f"Error getting budget history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/budget/reset")
async def reset_budget():
    """
    Reset monthly budget

    ⚠️  WARNING: Only use for testing/demo
    In production, this should be automated at month start
    """
    try:
        budget = get_budget_controller()
        budget.reset_monthly()
        return {
            "message": "Budget reset successfully",
            "new_status": budget.get_status()
        }

    except Exception as e:
        logger.error(f"Error resetting budget: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Utility Endpoints ====================

@app.post("/api/conversation/clear")
async def clear_conversation(conversation_id: str = "default"):
    """Clear conversation history"""
    try:
        ai_agent = get_ai_agent()
        ai_agent.clear_conversation(conversation_id)
        return {"message": f"Conversation '{conversation_id}' cleared"}

    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config")
async def get_config():
    """Get current configuration (non-sensitive)"""
    return {
        "mode": get_mode(),
        "budget_limit": settings.MONTHLY_BUDGET_LIMIT,
        "allowed_vm_sizes": settings.ALLOWED_VM_SIZES,
        "allowed_regions": settings.ALLOWED_REGIONS,
        "azure_configured": settings.AZURE_SUBSCRIPTION_ID is not None,
        "ai_configured": settings.OPENAI_API_KEY is not None,
    }


# ==================== Error Handlers ====================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return HTTPException(status_code=400, detail=str(exc))


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")


# ==================== Run Server ====================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
