"""
AI Agent with Function Calling

This is the BRAIN of the system.
Uses OpenAI's function calling feature to:
1. Understand user intent
2. Decide which function to call
3. Extract parameters from natural language
4. Execute the function
5. Format results for the user

NO HARDCODED IF/ELSE LOGIC NEEDED!
"""

import json
import logging
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI, OpenAI

from app.config import settings, get_mode, is_openai_configured
from app.azure_functions import get_resource_manager
from app.budget_control import get_budget_controller
from app.models import ChatResponse

logger = logging.getLogger(__name__)


class AIAgent:
    """
    AI-powered agent that uses function calling to control Azure

    How it works:
    1. User: "Create a small VM for testing"
    2. AI analyzes the message
    3. AI decides to call create_vm()
    4. AI extracts parameters: size="B1s", name="test-vm-..."
    5. Function executes
    6. AI formats the result for user

    No if/else logic needed - AI makes all decisions!
    """

    def __init__(self):
        """Initialize AI Agent"""
        self.mode = get_mode()
        self.resource_manager = get_resource_manager()
        self.budget = get_budget_controller()

        # Initialize OpenRouter client if configured
        if is_openai_configured():
            # OpenRouter uses OpenAI-compatible API
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                default_headers={
                    "HTTP-Referer": settings.APP_URL,
                    "X-Title": settings.APP_TITLE,
                }
            )
            self.sync_client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                default_headers={
                    "HTTP-Referer": settings.APP_URL,
                    "X-Title": settings.APP_TITLE,
                }
            )
            self.ai_enabled = True
            logger.info(f"✅ AI Agent initialized with OpenRouter ({settings.OPENAI_MODEL})")
        else:
            self.client = None
            self.sync_client = None
            self.ai_enabled = False
            logger.warning("⚠️  AI Agent initialized without OpenAI (fallback mode)")

        # Define available functions for AI
        self.tools = self._define_tools()

        # Conversation history (simple in-memory storage)
        self.conversations: Dict[str, List[Dict]] = {}

    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define available functions that AI can call

        This is KEY to function calling:
        - Good descriptions help AI choose the right function
        - Clear parameters help AI extract values from user message
        - Examples in descriptions improve accuracy
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_vm",
                    "description": """Create a virtual machine in Azure.
                    Use this when user wants to:
                    - Create a VM
                    - Create a server
                    - Spin up a machine
                    - Deploy a VM
                    Always use B1s size (smallest/cheapest).
                    Example: "Create a VM for testing" -> create_vm(name="test-vm-001", region="southeastasia")
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "VM name in lowercase with hyphens. Generate a name if not provided (e.g., 'test-vm-001', 'web-server-01')"
                            },
                            "region": {
                                "type": "string",
                                "enum": ["southeastasia", "eastasia"],
                                "description": "Azure region. Default to 'southeastasia' if not specified",
                                "default": "southeastasia"
                            },
                            "size": {
                                "type": "string",
                                "enum": ["B1s"],
                                "description": "VM size. Always use B1s (cheapest)",
                                "default": "B1s"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "stop_vm",
                    "description": """Stop (deallocate) a running VM to save money.
                    Use this when user wants to:
                    - Stop a VM
                    - Turn off a VM
                    - Deallocate a VM
                    - Save costs
                    Example: "Stop the test VM" -> stop_vm(name="test-vm-001")
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the VM to stop"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "start_vm",
                    "description": """Start a stopped VM.
                    Use when user wants to start, turn on, or resume a VM.
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the VM to start"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_vm",
                    "description": """Delete a VM permanently.
                    Use when user explicitly wants to delete or remove a VM.
                    Always confirm this is what they want.
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the VM to delete"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_resources",
                    "description": """List all VMs and resources.
                    Use when user wants to:
                    - See all VMs
                    - List resources
                    - Check what's running
                    - View current infrastructure
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_budget_status",
                    "description": """Get current budget and spending information.
                    Use when user asks about:
                    - Cost
                    - Budget
                    - Spending
                    - How much money used
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

    def _get_system_prompt(self) -> str:
        """Get system prompt for AI"""
        mode_info = {
            "mock": "You are in SIMULATION mode. All operations are simulated and no real Azure resources are created.",
            "azure": "You are in PRODUCTION mode. Operations will create real Azure resources and incur costs.",
            "unconfigured": "Azure is not configured. You can only provide information, not perform actions."
        }

        return f"""You are an expert Azure Cloud Engineer assistant.

CURRENT MODE: {self.mode.upper()}
{mode_info.get(self.mode, '')}

Your role:
- Help users manage Azure infrastructure through natural language
- Use function calling to execute operations
- Always consider cost optimization
- Explain what you're doing clearly
- Warn about costs before creating resources

Important guidelines:
1. ALWAYS use B1s VMs (cheapest option)
2. Prefer Southeast Asia region (closest to user)
3. Stop VMs when not in use to save money
4. Check budget before expensive operations
5. Generate descriptive VM names if user doesn't provide one

Budget Limit: ${self.budget.monthly_limit:.2f}/month
Current Spend: ${self.budget.current_spend:.2f}
Remaining: ${self.budget.remaining:.2f}

Be helpful, concise, and cost-conscious!
"""

    async def process(
        self,
        user_message: str,
        conversation_id: str = "default"
    ) -> ChatResponse:
        """
        Process user message and execute actions

        This is the main entry point for the AI agent.

        Args:
            user_message: Message from user
            conversation_id: Conversation ID for history tracking

        Returns:
            ChatResponse with AI's reply and any function results
        """
        logger.info(f"Processing message: {user_message[:50]}...")

        # If AI not configured, use fallback
        if not self.ai_enabled:
            return await self._fallback_response(user_message)

        # Get or create conversation history
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        conversation = self.conversations[conversation_id]

        # Add user message to history
        conversation.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Call OpenAI with function calling
            response = await self._call_openai(conversation)

            # Check if AI wants to call a function
            if response.choices[0].message.tool_calls:
                return await self._handle_function_call(
                    response,
                    conversation,
                    conversation_id
                )
            else:
                # AI just wants to talk
                ai_message = response.choices[0].message.content

                # Add to history
                conversation.append({
                    "role": "assistant",
                    "content": ai_message
                })

                return ChatResponse(
                    message=ai_message,
                    mode=self.mode
                )

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return ChatResponse(
                message=f"Sorry, I encountered an error: {str(e)}",
                mode=self.mode
            )

    async def _call_openai(self, messages: List[Dict]) -> Any:
        """Call OpenAI API with function calling enabled"""
        return await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                *messages
            ],
            tools=self.tools,
            tool_choice="auto",  # Let AI decide when to call functions
            temperature=0.7
        )

    async def _handle_function_call(
        self,
        response: Any,
        conversation: List[Dict],
        conversation_id: str
    ) -> ChatResponse:
        """Handle function call from AI"""
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        logger.info(f"AI decided to call: {function_name} with {arguments}")

        # Execute the function
        function_result = await self._execute_function(function_name, arguments)

        # Add assistant message with function call to history
        conversation.append(response.choices[0].message)

        # Add function result to history
        conversation.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(function_result)
        })

        # Get AI's final response
        final_response = await self._call_openai(conversation)
        final_message = final_response.choices[0].message.content

        # Add to history
        conversation.append({
            "role": "assistant",
            "content": final_message
        })

        return ChatResponse(
            message=final_message,
            function_called=function_name,
            function_result=function_result,
            mode=self.mode
        )

    async def _execute_function(
        self,
        function_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the requested function

        This maps AI function calls to actual Azure operations
        """
        try:
            if function_name == "create_vm":
                result = await self.resource_manager.create_vm(**arguments)
                return result.model_dump()

            elif function_name == "stop_vm":
                return await self.resource_manager.stop_vm(arguments["name"])

            elif function_name == "start_vm":
                return await self.resource_manager.start_vm(arguments["name"])

            elif function_name == "delete_vm":
                return await self.resource_manager.delete_vm(arguments["name"])

            elif function_name == "list_resources":
                resources = await self.resource_manager.list_all_resources()
                return {
                    "total_vms": resources.total_count,
                    "total_monthly_cost": resources.total_monthly_cost,
                    "vms": [vm.model_dump() for vm in resources.resources]
                }

            elif function_name == "get_budget_status":
                status = self.budget.get_status()
                return status.model_dump()

            else:
                return {
                    "success": False,
                    "error": f"Unknown function: {function_name}"
                }

        except Exception as e:
            logger.error(f"Error executing function {function_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _fallback_response(self, message: str) -> ChatResponse:
        """Fallback response when OpenAI is not configured"""
        return ChatResponse(
            message="AI is not configured. Please set OPENAI_API_KEY to use the AI agent. "
                    "You can still use the API endpoints directly to manage resources.",
            mode=self.mode
        )

    def clear_conversation(self, conversation_id: str = "default") -> None:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Cleared conversation: {conversation_id}")


# Global AI agent instance
ai_agent = AIAgent()


def get_ai_agent() -> AIAgent:
    """Get the global AI agent instance"""
    return ai_agent


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        agent = AIAgent()

        # Test messages
        test_messages = [
            "Create a small VM for testing",
            "What VMs do I have?",
            "What's my budget status?",
            "Stop the test VM",
        ]

        for msg in test_messages:
            print(f"\n{'='*50}")
            print(f"User: {msg}")
            response = await agent.process(msg)
            print(f"AI: {response.message}")
            if response.function_called:
                print(f"Function called: {response.function_called}")

    asyncio.run(main())
