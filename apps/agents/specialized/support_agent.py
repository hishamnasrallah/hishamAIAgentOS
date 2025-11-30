from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class SupportAgent(BaseAgent):
    """
    Customer Support Agent
    Specialized in helping users solve problems and answer questions.
    """

    agent_type = AgentType.SUPPORT
    agent_name = "Support Agent"
    agent_description = "Expert in customer support and problem resolution"
    capabilities = [
        "TROUBLESHOOTING",
        "QUESTION_ANSWERING",
        "TICKET_HANDLING",
        "DOCUMENTATION_SEARCH",
        "ESCALATION_MANAGEMENT"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Support task.

        Expected input_data:
            - task_type: TROUBLESHOOT | ANSWER | TICKET | ESCALATE | FEEDBACK
            - issue: User's issue or question
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'TROUBLESHOOT')
        issue = input_data.get('issue', '')
        user_context = input_data.get('user_context', {})
        context = input_data.get('context', {})

        logger.info(f"Executing Support task: {task_type}")

        user_message = self._build_support_prompt(task_type, issue, user_context, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'resolution': response
        }

    def _build_support_prompt(
        self,
        task_type: str,
        issue: str,
        user_context: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for support task."""

        if task_type == 'TROUBLESHOOT':
            return f"""
I need you to help troubleshoot this user issue.

User Issue:
{issue}

User Context:
{user_context if user_context else 'None'}

Please provide comprehensive troubleshooting:

1. **Issue Understanding** 🔍
   - What is the user trying to do?
   - What is actually happening?
   - Expected vs actual behavior

2. **Initial Questions** ❓
   If more information is needed, ask:
   - Clarifying questions
   - Environment details
   - Steps to reproduce

3. **Possible Causes** 🎯
   - Most likely causes (prioritized)
   - Known issues matching this
   - Similar past issues

4. **Troubleshooting Steps** 🛠️
   Step 1: [Action]
   - What to do
   - What to check
   - Expected result

   Step 2: [Action]
   - What to do
   - What to check
   - Expected result

   ...

5. **Solutions** ✅

   **Quick Fix** (if available):
   - Immediate workaround
   - Step-by-step instructions

   **Permanent Fix**:
   - Complete solution
   - Detailed instructions
   - Screenshots needed (describe)

6. **Verification** ✓
   - How to verify it's fixed
   - What to test
   - Expected outcome

7. **Prevention** 🛡️
   - How to avoid this in the future
   - Best practices
   - Configuration tips

8. **Escalation Criteria** ⚠️
   - When to escalate
   - What information to provide
   - Urgency level

Additional Context: {context if context else 'None'}
"""

        elif task_type == 'ANSWER':
            return f"""
I need you to answer this user question.

User Question:
{issue}

User Context:
{user_context if user_context else 'None'}

Please provide a helpful answer:

1. **Direct Answer** 💡
   - Clear, concise answer to the question
   - Address exactly what was asked

2. **Detailed Explanation** 📖
   - Provide context
   - Explain the "why"
   - Cover related concepts

3. **Step-by-Step Guide** 📋
   If applicable:
   - Step 1: [Action]
   - Step 2: [Action]
   - Step 3: [Action]
   - ...

4. **Examples** 💻
   - Practical examples
   - Code samples (if technical)
   - Screenshots needed (describe)

5. **Additional Resources** 🔗
   - Related documentation
   - Helpful articles
   - Video tutorials

6. **Common Pitfalls** ⚠️
   - What to avoid
   - Common mistakes
   - Best practices

7. **Follow-up** 🤝
   - Related questions they might have
   - Next steps
   - Further help available

Additional Context: {context if context else 'None'}
"""

        elif task_type == 'TICKET':
            return f"""
I need you to analyze and respond to this support ticket.

Ticket Details:
{issue}

User Context:
{user_context if user_context else 'None'}

Please provide ticket analysis and response:

1. **Ticket Classification** 🏷️
   - Category: Technical/Billing/Feature/Bug/Question
   - Priority: Critical/High/Medium/Low
   - Severity: How badly is the user blocked?
   - Type: Incident/Request/Question

2. **Impact Assessment** 📊
   - How many users affected?
   - Business impact
   - Urgency

3. **Root Cause** 🔍
   - What caused this issue?
   - Is it a known issue?
   - Related tickets?

4. **Response to User** 📧

   Subject: [Appropriate subject line]

   Hi [User],

   [Professional, empathetic response]

   [Clear explanation]

   [Solution or next steps]

   [Timeline if applicable]

   Best regards,
   Support Team

5. **Internal Notes** 📝
   - Technical details
   - Investigation findings
   - Actions taken

6. **Resolution Plan** 🎯
   - Immediate actions
   - Short-term fix
   - Long-term solution
   - Owner assignment

7. **Follow-up Actions** ✅
   - When to follow up
   - What to check
   - Closure criteria

Additional Context: {context if context else 'None'}
"""

        elif task_type == 'ESCALATE':
            return f"""
I need to prepare an escalation for this issue.

Issue:
{issue}

User Context:
{user_context if user_context else 'None'}

Please prepare escalation details:

1. **Escalation Summary** 📋
   - Brief overview of the issue
   - Why it needs escalation
   - Urgency level

2. **User Impact** 👥
   - Who is affected
   - How severe is the impact
   - Business implications

3. **Investigation Done** 🔍
   - Troubleshooting steps taken
   - What was ruled out
   - Current findings

4. **Technical Details** 🔧
   - System information
   - Error messages
   - Logs/Screenshots
   - Reproduction steps

5. **Requested Action** 🎯
   - What we need from the next level
   - Specific expertise needed
   - Expected timeline

6. **Workarounds** 🛠️
   - Temporary solutions provided
   - User communication
   - Mitigation in place

7. **Priority Justification** ⚠️
   - Why this priority level
   - SLA implications
   - Customer tier

8. **Communication Plan** 📢
   - User expectations set
   - Update frequency
   - Escalation path explained

Additional Context: {context if context else 'None'}
"""

        elif task_type == 'FEEDBACK':
            return f"""
I need you to analyze this user feedback.

Feedback:
{issue}

User Context:
{user_context if user_context else 'None'}

Please provide feedback analysis:

1. **Feedback Classification** 🏷️
   - Type: Bug/Feature Request/Complaint/Praise/Suggestion
   - Sentiment: Positive/Neutral/Negative
   - Priority: High/Medium/Low

2. **Key Points** 📝
   - Main feedback points
   - User pain points
   - Feature requests
   - Usability issues

3. **User Sentiment Analysis** 😊😐😞
   - Overall sentiment
   - Satisfaction level
   - Frustration indicators
   - Churn risk

4. **Actionable Insights** 💡
   - What to improve
   - Quick wins
   - Long-term changes
   - Product opportunities

5. **Response to User** 📧

   Hi [User],

   [Thank them for feedback]

   [Acknowledge their points]

   [What we're doing about it]

   [Next steps]

   Best regards,
   Support Team

6. **Internal Actions** 🎯
   - Product team notification
   - Feature request ticket
   - Bug ticket (if applicable)
   - Documentation update

7. **Trend Analysis** 📊
   - Similar feedback received?
   - Pattern identified?
   - Growing concern?

Additional Context: {context if context else 'None'}
"""

        else:
            return issue
