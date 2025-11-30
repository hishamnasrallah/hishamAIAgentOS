from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class ReleaseManagerAgent(BaseAgent):
    """
    Release Manager Agent
    Specialized in coordinating releases and managing deployment schedules.
    """

    agent_type = AgentType.RELEASE_MANAGER
    agent_name = "Release Manager Agent"
    agent_description = "Expert in release coordination and deployment management"
    capabilities = [
        "RELEASE_PLANNING",
        "DEPLOYMENT_COORDINATION",
        "ROLLBACK_MANAGEMENT",
        "RELEASE_NOTES",
        "POST_RELEASE_MONITORING"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Release Manager task.

        Expected input_data:
            - task_type: PLAN | DEPLOY | ROLLBACK | NOTES | MONITOR
            - release: Release details
            - requirements: Requirements
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'PLAN')
        release = input_data.get('release', '')
        requirements = input_data.get('requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Release Manager task: {task_type}")

        user_message = self._build_rm_prompt(task_type, release, requirements, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'release': release
        }

    def _build_rm_prompt(
        self,
        task_type: str,
        release: str,
        requirements: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for Release Manager task."""

        if task_type == 'PLAN':
            return f"""
I need you to create a comprehensive release plan.

Release:
{release}

Details:
{requirements}

Please provide:

1. **Release Overview**
   - Release version
   - Release date/timeline
   - Release scope
   - Key features

2. **Pre-Release Checklist**
   - Code freeze date
   - Testing completion
   - Documentation updates
   - Security review
   - Performance testing

3. **Deployment Strategy**
   - Deployment approach (blue-green, canary, rolling)
   - Environments (staging → production)
   - Deployment windows
   - Rollback plan

4. **Go/No-Go Criteria**
   - Quality gates
   - Test pass criteria
   - Performance benchmarks
   - Security requirements

5. **Communication Plan**
   - Stakeholder notifications
   - User communications
   - Internal team updates

6. **Risk Assessment**
   - Identified risks
   - Mitigation strategies
   - Contingency plans

Context: {context if context else 'None'}
"""

        elif task_type == 'DEPLOY':
            return f"""
I need you to coordinate the deployment.

Release:
{release}

Deployment Details:
{requirements}

Please provide:

1. **Deployment Checklist**
   - Pre-deployment verification
   - Deployment steps
   - Post-deployment verification
   - Smoke tests

2. **Deployment Timeline**
   - Start time
   - Expected duration
   - Key milestones
   - Completion time

3. **Team Coordination**
   - Roles and responsibilities
   - Communication channels
   - Escalation path

4. **Monitoring Plan**
   - Key metrics to watch
   - Alert thresholds
   - Monitoring duration

5. **Rollback Triggers**
   - When to rollback
   - Rollback procedure
   - Decision makers

Context: {context if context else 'None'}
"""

        elif task_type == 'ROLLBACK':
            return f"""
I need a rollback plan for this release.

Release:
{release}

Rollback Scenario:
{requirements}

Please provide:

1. **Rollback Assessment**
   - Reason for rollback
   - Impact analysis
   - Urgency level

2. **Rollback Procedure**
   - Step-by-step rollback steps
   - Database rollback (if needed)
   - Cache invalidation
   - Configuration rollback

3. **Verification Steps**
   - Post-rollback checks
   - System health verification
   - Data integrity checks

4. **Communication**
   - Who to notify
   - What to communicate
   - Status updates

5. **Post-Mortem Planning**
   - Root cause analysis
   - Lessons learned
   - Prevention measures

Context: {context if context else 'None'}
"""

        elif task_type == 'NOTES':
            return f"""
I need you to create release notes.

Release:
{release}

Release Details:
{requirements}

Please provide professional release notes:

1. **Release Header**
   - Version number
   - Release date
   - Release type (major/minor/patch)

2. **What's New** ✨
   - New features
   - Brief description of each
   - User benefits

3. **Improvements** 🚀
   - Performance improvements
   - UX enhancements
   - Other improvements

4. **Bug Fixes** 🐛
   - Fixed issues
   - Impact of fixes

5. **Breaking Changes** ⚠️
   - API changes
   - Migration required
   - Deprecations

6. **Known Issues** 📋
   - Outstanding issues
   - Workarounds

7. **Upgrade Guide** 📖
   - How to upgrade
   - Required actions
   - Rollback instructions

Context: {context if context else 'None'}
"""

        elif task_type == 'MONITOR':
            return f"""
I need help with post-release monitoring.

Release:
{release}

Monitoring Period:
{requirements}

Please provide:

1. **Key Metrics**
   - Performance metrics to track
   - Error rates
   - User activity
   - System health

2. **Success Criteria**
   - What indicates success
   - Acceptable thresholds
   - Red flags to watch

3. **Monitoring Schedule**
   - First hour
   - First 24 hours
   - First week
   - Ongoing

4. **Issue Response Plan**
   - How to triage issues
   - Escalation criteria
   - Response time SLAs

5. **Status Reporting**
   - Update frequency
   - Who to update
   - Report format

Context: {context if context else 'None'}
"""

        else:
            return requirements
