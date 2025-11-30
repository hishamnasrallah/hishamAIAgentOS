from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class ProjectManagerAgent(BaseAgent):
    """
    Project Manager Agent
    Specialized in project planning, risk management, and stakeholder coordination.
    """

    agent_type = AgentType.PM
    agent_name = "Project Manager Agent"
    agent_description = "Expert in project planning and coordination"
    capabilities = [
        "PROJECT_PLANNING",
        "TIMELINE_CREATION",
        "RISK_MANAGEMENT",
        "RESOURCE_ALLOCATION",
        "STAKEHOLDER_MANAGEMENT"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a PM task.

        Expected input_data:
            - task_type: PLAN | TIMELINE | RISKS | RESOURCES | STAKEHOLDERS
            - project: Project details
            - requirements: Requirements
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'PLAN')
        project = input_data.get('project', '')
        requirements = input_data.get('requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing PM task: {task_type}")

        user_message = self._build_pm_prompt(task_type, project, requirements, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'project': project
        }

    def _build_pm_prompt(
        self,
        task_type: str,
        project: str,
        requirements: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for PM task."""

        if task_type == 'PLAN':
            return f"""
I need you to create a comprehensive project plan.

Project:
{project}

Requirements:
{requirements}

Please provide:

1. **Project Overview**
   - Goals and objectives
   - Success criteria
   - Key deliverables

2. **Scope**
   - In scope
   - Out of scope
   - Assumptions
   - Constraints

3. **Timeline**
   - Project phases
   - Key milestones
   - Dependencies

4. **Resource Requirements**
   - Team composition
   - Skills needed
   - Tools and infrastructure

5. **Budget Estimation**
   - Development costs
   - Infrastructure costs
   - Contingency

6. **Risk Management**
   - Key risks
   - Mitigation strategies

7. **Communication Plan**
   - Stakeholders
   - Update frequency
   - Communication channels

Context: {context if context else 'None'}
"""

        elif task_type == 'TIMELINE':
            return f"""
I need you to create a detailed project timeline.

Project:
{project}

Requirements:
{requirements}

Please provide:
1. **Project Phases** with durations
2. **Key Milestones** with dates
3. **Task Breakdown** for each phase
4. **Dependencies** between tasks
5. **Critical Path** analysis
6. **Resource Allocation** timeline
7. **Buffer Time** for risks

Present as a Gantt chart format or table.

Context: {context if context else 'None'}
"""

        elif task_type == 'RISKS':
            return f"""
I need you to perform risk analysis for this project.

Project:
{project}

Details:
{requirements}

Please provide:

1. **Risk Identification**
   - Technical risks
   - Schedule risks
   - Resource risks
   - External risks

2. **Risk Assessment**
   For each risk:
   - Probability (High/Medium/Low)
   - Impact (High/Medium/Low)
   - Risk Score

3. **Mitigation Strategies**
   For each high-priority risk:
   - Prevention measures
   - Contingency plans
   - Owner

4. **Risk Monitoring Plan**

Context: {context if context else 'None'}
"""

        elif task_type == 'RESOURCES':
            return f"""
I need help with resource planning for this project.

Project:
{project}

Requirements:
{requirements}

Please provide:

1. **Team Structure**
   - Required roles
   - Team size
   - Reporting structure

2. **Resource Allocation**
   - FTE breakdown
   - Timeline per resource
   - Skill requirements

3. **Tools and Infrastructure**
   - Development tools
   - Infrastructure needs
   - Software licenses

4. **Budget**
   - Personnel costs
   - Infrastructure costs
   - Tool costs
   - Total budget

Context: {context if context else 'None'}
"""

        elif task_type == 'STAKEHOLDERS':
            return f"""
I need help with stakeholder management for this project.

Project:
{project}

Details:
{requirements}

Please provide:

1. **Stakeholder Identification**
   - Internal stakeholders
   - External stakeholders
   - Their interests and concerns

2. **Stakeholder Analysis**
   - Power/Interest matrix
   - Engagement level needed

3. **Communication Plan**
   - What to communicate
   - When to communicate
   - How to communicate
   - Frequency

4. **Engagement Strategy**
   - How to keep stakeholders engaged
   - Feedback mechanisms
   - Issue escalation

Context: {context if context else 'None'}
"""

        else:
            return requirements
