from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class BugTriageAgent(BaseAgent):
    """
    Bug Triage Agent
    Specialized in analyzing, categorizing, and prioritizing bugs.
    """

    agent_type = AgentType.BUG_TRIAGE
    agent_name = "Bug Triage Agent"
    agent_description = "Expert in bug analysis and prioritization"
    capabilities = [
        "BUG_ANALYSIS",
        "SEVERITY_ASSESSMENT",
        "PRIORITY_ASSIGNMENT",
        "ROOT_CAUSE_IDENTIFICATION",
        "FIX_RECOMMENDATION"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Bug Triage task.

        Expected input_data:
            - task_type: TRIAGE | ANALYZE | CATEGORIZE | RECOMMEND
            - bug_report: Bug details
            - code: (optional) Related code
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'TRIAGE')
        bug_report = input_data.get('bug_report', '')
        code = input_data.get('code', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Bug Triage task: {task_type}")

        user_message = self._build_triage_prompt(task_type, bug_report, code, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'severity': self._extract_severity(response),
            'priority': self._extract_priority(response)
        }

    def _build_triage_prompt(
        self,
        task_type: str,
        bug_report: str,
        code: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for bug triage task."""

        if task_type == 'TRIAGE':
            return f"""
I need you to triage this bug report.

Bug Report:
{bug_report}

{f"Related Code:\n```\n{code}\n```\n" if code else ""}

Please provide comprehensive bug triage:

1. **Bug Summary**
   - Clear, concise description
   - Affected component/feature

2. **Severity Assessment** ⚠️
   - **Critical**: System down, data loss, security breach
   - **High**: Major feature broken, severe impact
   - **Medium**: Feature partially working, workaround exists
   - **Low**: Minor issue, cosmetic problem

   Selected: [Your assessment]
   Justification: [Why?]

3. **Priority Assignment** 🎯
   - **P0**: Fix immediately (< 24 hours)
   - **P1**: Fix in current sprint
   - **P2**: Fix in next sprint
   - **P3**: Backlog

   Selected: [Your assessment]
   Justification: [Why?]

4. **Category**
   - Bug type (functional, performance, security, UI, etc.)
   - Affected area
   - Environment

5. **Impact Analysis** 📊
   - Number of users affected
   - Business impact
   - Technical impact

6. **Reproducibility**
   - Always / Sometimes / Rarely
   - Steps to reproduce
   - Environment details

7. **Root Cause Hypothesis**
   - Likely cause
   - Related issues
   - Technical analysis

8. **Recommended Actions** 💡
   - Investigation steps
   - Potential fixes
   - Workarounds
   - Owner recommendation

Context: {context if context else 'None'}
"""

        elif task_type == 'ANALYZE':
            return f"""
I need deep analysis of this bug.

Bug Report:
{bug_report}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please provide:

1. **Root Cause Analysis**
   - What is causing the bug?
   - Why did it happen?
   - When was it introduced?

2. **Code Analysis**
   - Problematic code section
   - Logic errors
   - Edge cases not handled

3. **Impact Assessment**
   - Direct impact
   - Indirect impact
   - Cascading effects

4. **Related Issues**
   - Similar bugs
   - Dependencies
   - Patterns

5. **Fix Complexity**
   - Simple / Medium / Complex
   - Estimated effort
   - Risks in fixing

Context: {context if context else 'None'}
"""

        elif task_type == 'CATEGORIZE':
            return f"""
I need you to categorize and organize these bugs.

Bug Reports:
{bug_report}

Please provide:

1. **Bug Categories**
   - Group by type (functional, performance, security, UI)
   - Group by component
   - Group by severity

2. **Patterns Identified**
   - Common root causes
   - Frequently affected areas
   - Recurring issues

3. **Prioritization**
   - Must fix now
   - Should fix soon
   - Can fix later
   - Won't fix (with reason)

4. **Resource Planning**
   - Which bugs to batch together
   - Skill requirements
   - Estimated effort

Context: {context if context else 'None'}
"""

        elif task_type == 'RECOMMEND':
            return f"""
I need fix recommendations for this bug.

Bug Report:
{bug_report}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please provide:

1. **Recommended Fix** ✅
   - Detailed solution approach
   - Code changes needed
   - Configuration changes

2. **Alternative Approaches**
   - Other ways to fix
   - Pros and cons of each

3. **Testing Strategy**
   - How to verify the fix
   - Test cases to add
   - Regression testing

4. **Prevention** 🛡️
   - How to prevent similar bugs
   - Code improvements
   - Process improvements

5. **Implementation Plan**
   - Step-by-step fix process
   - Estimated time
   - Risk mitigation

Context: {context if context else 'None'}
"""

        else:
            return bug_report

    def _extract_severity(self, response: str) -> str:
        """Extract severity from response."""
        severity_map = {
            'critical': 'CRITICAL',
            'high': 'HIGH',
            'medium': 'MEDIUM',
            'low': 'LOW'
        }

        response_lower = response.lower()
        for key, value in severity_map.items():
            if f'severity: {key}' in response_lower or f'severity**: {key}' in response_lower:
                return value

        return 'MEDIUM'

    def _extract_priority(self, response: str) -> str:
        """Extract priority from response."""
        priority_map = {
            'p0': 'P0',
            'p1': 'P1',
            'p2': 'P2',
            'p3': 'P3'
        }

        response_lower = response.lower()
        for key, value in priority_map.items():
            if f'priority: {key}' in response_lower or f'priority**: {key}' in response_lower:
                return value

        return 'P2'
