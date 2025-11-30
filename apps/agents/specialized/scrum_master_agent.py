from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class ScrumMasterAgent(BaseAgent):
    """
    Scrum Master Agent
    Specialized in facilitating agile ceremonies and improving team productivity.
    """

    agent_type = AgentType.SCRUM_MASTER
    agent_name = "Scrum Master Agent"
    agent_description = "Expert in agile facilitation and team productivity"
    capabilities = [
        "SPRINT_PLANNING",
        "DAILY_STANDUP_FACILITATION",
        "RETROSPECTIVE_FACILITATION",
        "BLOCKER_REMOVAL",
        "TEAM_IMPROVEMENT"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Scrum Master task.

        Expected input_data:
            - task_type: SPRINT_PLAN | STANDUP | RETRO | BLOCKER | IMPROVEMENT
            - team_context: Team context
            - requirements: Requirements
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'SPRINT_PLAN')
        team_context = input_data.get('team_context', '')
        requirements = input_data.get('requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Scrum Master task: {task_type}")

        user_message = self._build_sm_prompt(task_type, team_context, requirements, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'team_context': team_context
        }

    def _build_sm_prompt(
        self,
        task_type: str,
        team_context: str,
        requirements: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for Scrum Master task."""

        if task_type == 'SPRINT_PLAN':
            return f"""
I need you to facilitate sprint planning.

Team Context:
{team_context}

Sprint Details:
{requirements}

Please provide:

1. **Sprint Goal**
   - Clear, achievable sprint goal
   - How it aligns with product goals

2. **Sprint Backlog**
   - Selected user stories
   - Task breakdown
   - Capacity planning

3. **Definition of Done**
   - Clear acceptance criteria
   - Quality standards

4. **Team Capacity**
   - Available hours
   - Team velocity
   - Risk factors

5. **Dependencies**
   - External dependencies
   - Mitigation plan

6. **Sprint Commitment**
   - What team commits to deliver
   - Confidence level

Context: {context if context else 'None'}
"""

        elif task_type == 'STANDUP':
            return f"""
I need help facilitating daily standup.

Team Context:
{team_context}

Standup Notes:
{requirements}

Please provide:

1. **Summary of Updates**
   - What was completed
   - What's in progress
   - What's planned

2. **Blockers Identified**
   - List of blockers
   - Impact assessment
   - Action plan for each

3. **Coordination Needs**
   - Team members who need to sync
   - Integration points

4. **Sprint Progress**
   - Burndown status
   - On track / At risk
   - Adjustment needed

5. **Action Items**
   - Clear, assigned actions
   - Deadlines

Context: {context if context else 'None'}
"""

        elif task_type == 'RETRO':
            return f"""
I need you to facilitate a sprint retrospective.

Team Context:
{team_context}

Sprint Review:
{requirements}

Please provide a structured retrospective:

1. **What Went Well** ✅
   - Successes
   - Positive highlights
   - Good practices to continue

2. **What Didn't Go Well** ❌
   - Challenges faced
   - Pain points
   - Bottlenecks

3. **Insights & Learnings** 💡
   - Key takeaways
   - Root cause analysis
   - Patterns observed

4. **Action Items** 🎯
   - Concrete improvement actions
   - Owner assigned
   - Success criteria
   - Due date

5. **Metrics Review** 📊
   - Velocity
   - Quality metrics
   - Team morale

Context: {context if context else 'None'}
"""

        elif task_type == 'BLOCKER':
            return f"""
I need help with blocker removal.

Team Context:
{team_context}

Blocker Details:
{requirements}

Please provide:

1. **Blocker Analysis**
   - Type of blocker (technical, organizational, external)
   - Root cause
   - Impact on sprint

2. **Severity Assessment**
   - Critical / High / Medium / Low
   - Urgency

3. **Resolution Strategy**
   - Immediate actions
   - Who needs to be involved
   - Alternative approaches

4. **Escalation Plan**
   - When to escalate
   - To whom
   - What information to provide

5. **Prevention**
   - How to prevent similar blockers
   - Process improvements

Context: {context if context else 'None'}
"""

        elif task_type == 'IMPROVEMENT':
            return f"""
I need suggestions for team improvement.

Team Context:
{team_context}

Current Situation:
{requirements}

Please provide:

1. **Current State Analysis**
   - Team strengths
   - Areas for improvement
   - Observed patterns

2. **Improvement Opportunities**
   - Process improvements
   - Tool improvements
   - Practice improvements

3. **Recommendations**
   - Prioritized recommendations
   - Implementation approach
   - Expected impact

4. **Change Management**
   - How to introduce changes
   - Addressing resistance
   - Measuring success

5. **Action Plan**
   - Step-by-step plan
   - Timeline
   - Success metrics

Context: {context if context else 'None'}
"""

        else:
            return requirements
