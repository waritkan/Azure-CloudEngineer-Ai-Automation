"""
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


# ==================== Request Models ====================

class ChatRequest(BaseModel):
    """Chat message from user"""
    message: str = Field(..., min_length=1, max_length=500)
    conversation_id: Optional[str] = None

    @validator('message')
    def validate_message(cls, v):
        """Ensure message is not just whitespace"""
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class CreateVMRequest(BaseModel):
    """Request to create a virtual machine"""
    name: str = Field(..., min_length=3, max_length=15)
    size: str = "B1s"
    region: str = "southeastasia"

    @validator('name')
    def validate_name(cls, v):
        """VM name must be lowercase alphanumeric with hyphens"""
        if not re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$', v):
            raise ValueError(
                'VM name must be lowercase, alphanumeric, and can contain hyphens'
            )
        return v

    @validator('size')
    def validate_size(cls, v):
        """Only allow B1s for cost control"""
        allowed = ["B1s"]
        if v not in allowed:
            raise ValueError(f'VM size must be one of: {", ".join(allowed)}')
        return v

    @validator('region')
    def validate_region(cls, v):
        """Only allow specific regions"""
        allowed = ["southeastasia", "eastasia"]
        if v not in allowed:
            raise ValueError(f'Region must be one of: {", ".join(allowed)}')
        return v


class VMActionRequest(BaseModel):
    """Request to perform action on VM (start/stop/delete)"""
    vm_name: str = Field(..., min_length=3)
    action: str = Field(..., pattern="^(start|stop|delete)$")


# ==================== Response Models ====================

class ChatResponse(BaseModel):
    """Response from AI chat"""
    message: str
    function_called: Optional[str] = None
    function_result: Optional[Dict[str, Any]] = None
    mode: str = "mock"  # mock or azure


class VMInfo(BaseModel):
    """Virtual machine information"""
    name: str
    size: str
    region: str
    status: str  # running, stopped, deallocated
    cost_per_hour: float
    cost_per_month: float
    created_at: Optional[str] = None


class VMCreateResponse(BaseModel):
    """Response after creating a VM"""
    success: bool
    vm_name: str
    status: str
    message: str
    estimated_cost: Dict[str, float]
    mode: str = "mock"


class BudgetStatus(BaseModel):
    """Current budget status"""
    limit: float
    current_spend: float
    remaining: float
    percentage_used: float
    operations_count: int
    last_updated: str


class ResourceListResponse(BaseModel):
    """List of all resources"""
    resources: List[VMInfo]
    total_count: int
    total_monthly_cost: float


class FunctionCallResult(BaseModel):
    """Result from a function execution"""
    success: bool
    function_name: str
    result: Dict[str, Any]
    error: Optional[str] = None
    mode: str = "mock"


# ==================== Internal Models ====================

class Operation(BaseModel):
    """Record of an operation for logging"""
    operation: str
    timestamp: datetime
    estimated_cost: float
    actual_cost: float = 0.0
    mode: str = "mock"
    parameters: Dict[str, Any] = {}
    result: Optional[str] = None


class AzureVMConfig(BaseModel):
    """Configuration for Azure VM creation"""
    vm_name: str
    resource_group: str
    location: str
    vm_size: str
    admin_username: str = "azureuser"
    # Note: In production, use SSH keys instead of password
    admin_password: Optional[str] = None
    os_type: str = "Linux"
    os_offer: str = "UbuntuServer"
    os_sku: str = "18.04-LTS"


# ==================== Error Models ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class ValidationError(BaseModel):
    """Validation error details"""
    field: str
    message: str
    type: str


# ==================== Example Data for Development ====================

def get_example_vm() -> VMInfo:
    """Get example VM for mock mode"""
    return VMInfo(
        name="test-vm-001",
        size="B1s",
        region="southeastasia",
        status="running",
        cost_per_hour=0.0104,
        cost_per_month=7.59,
        created_at=datetime.now().isoformat()
    )


def get_example_budget() -> BudgetStatus:
    """Get example budget status"""
    return BudgetStatus(
        limit=10.0,
        current_spend=2.5,
        remaining=7.5,
        percentage_used=25.0,
        operations_count=3,
        last_updated=datetime.now().isoformat()
    )
