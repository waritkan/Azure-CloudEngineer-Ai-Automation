"""
Azure Resource Management Functions

Provides abstraction layer for Azure operations with:
- Mock mode for development/demo
- Real Azure SDK integration for production
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from app.config import settings, get_mode, is_azure_configured
from app.models import VMInfo, VMCreateResponse, ResourceListResponse
from app.budget_control import get_budget_controller

logger = logging.getLogger(__name__)


class AzureResourceManager:
    """
    Manages Azure resources with mock/real mode support

    In Mock Mode:
    - Simulates Azure operations
    - No actual Azure API calls
    - No cost incurred
    - Perfect for development and demo

    In Azure Mode:
    - Real Azure SDK calls
    - Actual resource creation
    - Real costs apply
    - Requires Azure credentials
    """

    def __init__(self):
        """Initialize Azure Resource Manager"""
        self.mode = get_mode()
        self.budget = get_budget_controller()

        # Mock storage for simulated resources
        self.mock_vms: Dict[str, VMInfo] = {}

        # Initialize Azure clients if configured
        if self.mode == "azure":
            self._init_azure_clients()
        else:
            self.compute_client = None
            self.resource_client = None

        logger.info(f"Azure Resource Manager initialized in '{self.mode}' mode")

    def _init_azure_clients(self):
        """Initialize real Azure SDK clients"""
        try:
            from azure.identity import ClientSecretCredential
            from azure.mgmt.compute import ComputeManagementClient
            from azure.mgmt.resource import ResourceManagementClient

            credential = ClientSecretCredential(
                tenant_id=settings.AZURE_TENANT_ID,
                client_id=settings.AZURE_CLIENT_ID,
                client_secret=settings.AZURE_CLIENT_SECRET
            )

            self.compute_client = ComputeManagementClient(
                credential,
                settings.AZURE_SUBSCRIPTION_ID
            )

            self.resource_client = ResourceManagementClient(
                credential,
                settings.AZURE_SUBSCRIPTION_ID
            )

            logger.info("✅ Azure clients initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize Azure clients: {e}")
            raise

    async def create_vm(
        self,
        name: str,
        region: str = "southeastasia",
        size: str = "B1s"
    ) -> VMCreateResponse:
        """
        Create a virtual machine

        Args:
            name: VM name (lowercase, alphanumeric, hyphens)
            region: Azure region
            size: VM size (only B1s allowed)

        Returns:
            VMCreateResponse with creation details
        """
        logger.info(f"Creating VM: {name} ({size}) in {region}")

        # 1. Validate parameters
        if size not in settings.ALLOWED_VM_SIZES:
            raise ValueError(f"VM size '{size}' not allowed. Use: {settings.ALLOWED_VM_SIZES}")

        if region not in settings.ALLOWED_REGIONS:
            raise ValueError(f"Region '{region}' not allowed. Use: {settings.ALLOWED_REGIONS}")

        # 2. Estimate cost
        cost_estimate = self.budget.estimate_vm_cost(size)

        # 3. Check budget (for monthly cost)
        approved, reason = self.budget.check_and_approve(
            operation="create_vm",
            estimated_cost=cost_estimate["monthly"],
            parameters={"name": name, "size": size, "region": region}
        )

        if not approved:
            logger.warning(f"VM creation denied: {reason}")
            return VMCreateResponse(
                success=False,
                vm_name=name,
                status="denied",
                message=f"Budget exceeded: {reason}",
                estimated_cost=cost_estimate,
                mode=self.mode
            )

        # 4. Create VM (mock or real)
        if self.mode == "mock":
            result = await self._create_vm_mock(name, region, size, cost_estimate)
        else:
            result = await self._create_vm_azure(name, region, size, cost_estimate)

        # 5. Record operation
        self.budget.record_operation(
            operation="create_vm",
            estimated_cost=cost_estimate["monthly"],
            parameters={"name": name, "size": size, "region": region},
            result="success" if result.success else "failed",
            mode=self.mode
        )

        return result

    async def _create_vm_mock(
        self,
        name: str,
        region: str,
        size: str,
        cost_estimate: Dict[str, float]
    ) -> VMCreateResponse:
        """Mock VM creation (simulation only)"""
        logger.info(f"🎭 MOCK: Creating VM {name}")

        # Simulate API delay
        await asyncio.sleep(0.5)

        # Check if VM already exists
        if name in self.mock_vms:
            return VMCreateResponse(
                success=False,
                vm_name=name,
                status="error",
                message=f"VM '{name}' already exists",
                estimated_cost=cost_estimate,
                mode="mock"
            )

        # Create mock VM
        vm = VMInfo(
            name=name,
            size=size,
            region=region,
            status="running",
            cost_per_hour=cost_estimate["hourly"],
            cost_per_month=cost_estimate["monthly"],
            created_at=datetime.now().isoformat()
        )

        self.mock_vms[name] = vm

        logger.info(f"✅ MOCK: VM {name} created successfully")

        return VMCreateResponse(
            success=True,
            vm_name=name,
            status="running",
            message=f"VM '{name}' created successfully (SIMULATED)",
            estimated_cost=cost_estimate,
            mode="mock"
        )

    async def _create_vm_azure(
        self,
        name: str,
        region: str,
        size: str,
        cost_estimate: Dict[str, float]
    ) -> VMCreateResponse:
        """Real Azure VM creation"""
        logger.info(f"☁️  AZURE: Creating VM {name}")

        try:
            # Note: This is a simplified version
            # Production code would need more configuration

            vm_parameters = {
                'location': region,
                'os_profile': {
                    'computer_name': name,
                    'admin_username': 'azureuser',
                    'admin_password': 'TempPassword123!'  # Use SSH keys in production!
                },
                'hardware_profile': {
                    'vm_size': size
                },
                'storage_profile': {
                    'image_reference': {
                        'publisher': 'Canonical',
                        'offer': 'UbuntuServer',
                        'sku': '18.04-LTS',
                        'version': 'latest'
                    }
                },
                'network_profile': {
                    'network_interfaces': []  # Would need to create NIC first
                }
            }

            # Start async operation
            async_vm_creation = self.compute_client.virtual_machines.begin_create_or_update(
                settings.AZURE_RESOURCE_GROUP,
                name,
                vm_parameters
            )

            # Wait for completion
            vm_result = async_vm_creation.result()

            logger.info(f"✅ AZURE: VM {name} created successfully")

            return VMCreateResponse(
                success=True,
                vm_name=name,
                status="running",
                message=f"VM '{name}' created successfully in Azure",
                estimated_cost=cost_estimate,
                mode="azure"
            )

        except Exception as e:
            logger.error(f"❌ AZURE: Failed to create VM: {e}")
            return VMCreateResponse(
                success=False,
                vm_name=name,
                status="error",
                message=f"Failed to create VM: {str(e)}",
                estimated_cost=cost_estimate,
                mode="azure"
            )

    async def stop_vm(self, name: str) -> Dict[str, Any]:
        """
        Stop (deallocate) a virtual machine to save costs

        Args:
            name: VM name

        Returns:
            Result dictionary
        """
        logger.info(f"Stopping VM: {name}")

        if self.mode == "mock":
            return await self._stop_vm_mock(name)
        else:
            return await self._stop_vm_azure(name)

    async def _stop_vm_mock(self, name: str) -> Dict[str, Any]:
        """Mock VM stop"""
        if name not in self.mock_vms:
            return {
                "success": False,
                "message": f"VM '{name}' not found",
                "mode": "mock"
            }

        self.mock_vms[name].status = "stopped"
        logger.info(f"✅ MOCK: VM {name} stopped")

        return {
            "success": True,
            "message": f"VM '{name}' stopped successfully (SIMULATED)",
            "mode": "mock"
        }

    async def _stop_vm_azure(self, name: str) -> Dict[str, Any]:
        """Real Azure VM stop"""
        try:
            async_vm_stop = self.compute_client.virtual_machines.begin_deallocate(
                settings.AZURE_RESOURCE_GROUP,
                name
            )
            async_vm_stop.result()

            logger.info(f"✅ AZURE: VM {name} stopped")

            return {
                "success": True,
                "message": f"VM '{name}' stopped successfully",
                "mode": "azure"
            }

        except Exception as e:
            logger.error(f"❌ AZURE: Failed to stop VM: {e}")
            return {
                "success": False,
                "message": f"Failed to stop VM: {str(e)}",
                "mode": "azure"
            }

    async def start_vm(self, name: str) -> Dict[str, Any]:
        """Start a stopped virtual machine"""
        logger.info(f"Starting VM: {name}")

        if self.mode == "mock":
            if name not in self.mock_vms:
                return {"success": False, "message": f"VM '{name}' not found"}

            self.mock_vms[name].status = "running"
            return {
                "success": True,
                "message": f"VM '{name}' started (SIMULATED)",
                "mode": "mock"
            }
        else:
            try:
                async_vm_start = self.compute_client.virtual_machines.begin_start(
                    settings.AZURE_RESOURCE_GROUP,
                    name
                )
                async_vm_start.result()
                return {
                    "success": True,
                    "message": f"VM '{name}' started",
                    "mode": "azure"
                }
            except Exception as e:
                return {"success": False, "message": str(e), "mode": "azure"}

    async def delete_vm(self, name: str) -> Dict[str, Any]:
        """Delete a virtual machine"""
        logger.info(f"Deleting VM: {name}")

        if self.mode == "mock":
            if name not in self.mock_vms:
                return {"success": False, "message": f"VM '{name}' not found"}

            del self.mock_vms[name]
            return {
                "success": True,
                "message": f"VM '{name}' deleted (SIMULATED)",
                "mode": "mock"
            }
        else:
            try:
                async_vm_delete = self.compute_client.virtual_machines.begin_delete(
                    settings.AZURE_RESOURCE_GROUP,
                    name
                )
                async_vm_delete.result()
                return {
                    "success": True,
                    "message": f"VM '{name}' deleted",
                    "mode": "azure"
                }
            except Exception as e:
                return {"success": False, "message": str(e), "mode": "azure"}

    async def list_all_resources(self) -> ResourceListResponse:
        """List all virtual machines"""
        logger.info("Listing all VMs")

        if self.mode == "mock":
            vms = list(self.mock_vms.values())
        else:
            vms = await self._list_vms_azure()

        total_cost = sum(vm.cost_per_month for vm in vms)

        return ResourceListResponse(
            resources=vms,
            total_count=len(vms),
            total_monthly_cost=round(total_cost, 2)
        )

    async def _list_vms_azure(self) -> List[VMInfo]:
        """List VMs from Azure"""
        try:
            vms = []
            for vm in self.compute_client.virtual_machines.list(settings.AZURE_RESOURCE_GROUP):
                # Get cost estimate
                cost = self.budget.estimate_vm_cost(vm.hardware_profile.vm_size)

                vms.append(VMInfo(
                    name=vm.name,
                    size=vm.hardware_profile.vm_size,
                    region=vm.location,
                    status="running",  # Would need to check power state
                    cost_per_hour=cost["hourly"],
                    cost_per_month=cost["monthly"]
                ))

            return vms

        except Exception as e:
            logger.error(f"Failed to list VMs: {e}")
            return []

    async def get_vm_info(self, name: str) -> Optional[VMInfo]:
        """Get information about a specific VM"""
        if self.mode == "mock":
            return self.mock_vms.get(name)
        else:
            # Would query Azure for VM details
            pass


# Global resource manager instance
resource_manager = AzureResourceManager()


def get_resource_manager() -> AzureResourceManager:
    """Get the global resource manager instance"""
    return resource_manager


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        rm = AzureResourceManager()

        # Create a VM
        result = await rm.create_vm(
            name="test-vm-001",
            region="southeastasia",
            size="B1s"
        )
        print(f"Create result: {result}")

        # List VMs
        resources = await rm.list_all_resources()
        print(f"Total VMs: {resources.total_count}")
        print(f"Total cost: ${resources.total_monthly_cost}/month")

        # Stop VM
        stop_result = await rm.stop_vm("test-vm-001")
        print(f"Stop result: {stop_result}")

    asyncio.run(main())
