from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class DevOpsAgent(BaseAgent):
    """
    DevOps Engineer Agent
    Specialized in infrastructure, CI/CD, deployment, and operations.
    """

    agent_type = AgentType.DEVOPS
    agent_name = "DevOps Agent"
    agent_description = "Expert in infrastructure, deployment, and operations"
    capabilities = [
        "INFRASTRUCTURE_DESIGN",
        "CI_CD_SETUP",
        "DEPLOYMENT_AUTOMATION",
        "MONITORING_SETUP",
        "TROUBLESHOOTING"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a DevOps task.

        Expected input_data:
            - task_type: INFRA_DESIGN | CI_CD | DEPLOY | MONITOR | TROUBLESHOOT
            - technology: Docker, Kubernetes, AWS, etc.
            - requirements: Task requirements
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'DEPLOY')
        technology = input_data.get('technology', '')
        requirements = input_data.get('requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing DevOps task: {task_type}")

        user_message = self._build_devops_prompt(task_type, technology, requirements, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'technology': technology
        }

    def _build_devops_prompt(
        self,
        task_type: str,
        technology: str,
        requirements: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for DevOps task."""

        if task_type == 'INFRA_DESIGN':
            return f"""
I need you to design infrastructure for the following requirements:

Requirements:
{requirements}

Technology: {technology if technology else 'Your choice'}

Please provide:
1. Architecture diagram description
2. Infrastructure components
3. Scalability considerations
4. Security measures
5. Cost estimation
6. Technology stack recommendations

Context: {context if context else 'None'}
"""

        elif task_type == 'CI_CD':
            return f"""
I need you to set up CI/CD pipeline.

Requirements:
{requirements}

Technology: {technology}

Please provide:
1. CI/CD workflow configuration
2. Build steps
3. Testing stages
4. Deployment stages
5. Environment variables needed
6. Security best practices

Context: {context if context else 'None'}
"""

        elif task_type == 'DEPLOY':
            return f"""
I need help with deployment automation.

Requirements:
{requirements}

Technology: {technology}

Please provide:
1. Deployment scripts
2. Configuration files
3. Rollback strategy
4. Health checks
5. Blue-green/Canary deployment approach

Context: {context if context else 'None'}
"""

        elif task_type == 'MONITOR':
            return f"""
I need to set up monitoring and alerting.

Requirements:
{requirements}

Technology: {technology}

Please provide:
1. Monitoring setup
2. Key metrics to track
3. Alert rules
4. Dashboards configuration
5. Log aggregation setup

Context: {context if context else 'None'}
"""

        elif task_type == 'TROUBLESHOOT':
            return f"""
I need help troubleshooting an infrastructure issue.

Problem:
{requirements}

Technology: {technology}

Please provide:
1. Root cause analysis
2. Debugging steps
3. Solution
4. Preventive measures
5. Monitoring recommendations

Context: {context if context else 'None'}
"""

        else:
            return requirements
