from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from django.utils import timezone
from libs.ai_providers import AIProviderBase
from libs.ai_providers.base import Message
from .models import AgentTask, AgentExecution, Prompt, AIProvider, AgentType
import logging
import time

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all AI agents in HishamOS.
    Each specialized agent must inherit from this class.
    """

    agent_type: AgentType = None
    agent_name: str = "Base Agent"
    agent_description: str = "Base agent class"
    capabilities: List[str] = []

    def __init__(self, provider: AIProviderBase, prompt: Prompt):
        self.provider = provider
        self.prompt = prompt
        self.conversation_history: List[Message] = []

    @abstractmethod
    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute the given task and return the result.

        Args:
            task: The AgentTask to execute

        Returns:
            Dictionary containing the result of the task execution
        """
        pass

    def generate_response(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> str:
        """
        Generate a response using the AI provider.

        Args:
            user_message: The user's message/input
            context: Optional context dictionary
            stream: Whether to stream the response

        Returns:
            The generated response text
        """
        try:
            self.conversation_history.append(Message(role="user", content=user_message))

            if context:
                context_str = self._format_context(context)
                enhanced_message = f"{context_str}\n\n{user_message}"
                self.conversation_history[-1].content = enhanced_message

            response = self.provider.generate(
                messages=self.conversation_history,
                system_prompt=self.prompt.system_prompt
            )

            self.conversation_history.append(
                Message(role="assistant", content=response.content)
            )

            return response.content

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary into a readable string."""
        lines = ["Context:"]
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def run_with_tracking(self, task: AgentTask, provider_instance: AIProvider) -> Dict[str, Any]:
        """
        Execute task with full tracking and logging.

        Args:
            task: The AgentTask to execute
            provider_instance: The AIProvider model instance

        Returns:
            Task execution result
        """
        execution = AgentExecution.objects.create(
            task=task,
            agent_type=self.agent_type,
            provider=provider_instance,
            prompt_used=self.prompt
        )

        start_time = time.time()
        task.status = 'IN_PROGRESS'
        task.started_at = timezone.now()
        task.save()

        try:
            result = self.execute_task(task)

            execution_time = time.time() - start_time
            execution.execution_time_seconds = execution_time
            execution.success = True
            execution.raw_response = result
            execution.save()

            task.status = 'COMPLETED'
            task.completed_at = timezone.now()
            task.execution_time_seconds = execution_time
            task.output_data = result
            task.save()

            logger.info(f"Task {task.id} completed successfully in {execution_time:.2f}s")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)

            execution.execution_time_seconds = execution_time
            execution.success = False
            execution.error_message = error_msg
            execution.save()

            task.status = 'FAILED'
            task.error_message = error_msg
            task.execution_time_seconds = execution_time
            task.save()

            logger.error(f"Task {task.id} failed: {error_msg}")
            raise


class AgentFactory:
    """Factory class to create agent instances."""

    _agent_registry: Dict[str, type] = {}
    _initialized = False

    @classmethod
    def _initialize_registry(cls):
        """Initialize the agent registry with all available agents."""
        if cls._initialized:
            return

        from .specialized import (
            CodingAgent, CodeReviewAgent, BusinessAnalystAgent,
            DevOpsAgent, QAAgent, ProjectManagerAgent, ScrumMasterAgent,
            ReleaseManagerAgent, BugTriageAgent, SecurityAgent,
            PerformanceAgent, DocumentationAgent, UIUXAgent,
            DataAnalystAgent, SupportAgent
        )

        cls._agent_registry = {
            AgentType.CODING: CodingAgent,
            AgentType.CODE_REVIEW: CodeReviewAgent,
            AgentType.BA: BusinessAnalystAgent,
            AgentType.DEVOPS: DevOpsAgent,
            AgentType.QA: QAAgent,
            AgentType.PM: ProjectManagerAgent,
            AgentType.SCRUM_MASTER: ScrumMasterAgent,
            AgentType.RELEASE_MANAGER: ReleaseManagerAgent,
            AgentType.BUG_TRIAGE: BugTriageAgent,
            AgentType.SECURITY: SecurityAgent,
            AgentType.PERFORMANCE: PerformanceAgent,
            AgentType.DOCUMENTATION: DocumentationAgent,
            AgentType.UI_UX: UIUXAgent,
            AgentType.DATA_ANALYST: DataAnalystAgent,
            AgentType.SUPPORT: SupportAgent,
        }
        cls._initialized = True

    @classmethod
    def register_agent(cls, agent_type: AgentType, agent_class: type):
        """Register an agent class."""
        cls._agent_registry[agent_type] = agent_class

    @classmethod
    def create_agent(
        cls,
        agent_type: AgentType,
        provider: AIProviderBase,
        prompt: Prompt
    ) -> BaseAgent:
        """Create an agent instance."""
        cls._initialize_registry()
        agent_class = cls._agent_registry.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return agent_class(provider, prompt)

    @classmethod
    def get_available_agents(cls) -> List[str]:
        """Get list of registered agent types."""
        cls._initialize_registry()
        return list(cls._agent_registry.keys())
