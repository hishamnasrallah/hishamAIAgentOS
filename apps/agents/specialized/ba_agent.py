from typing import Dict, Any, List
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class BusinessAnalystAgent(BaseAgent):
    """
    Business Analyst Agent
    Specialized in requirements gathering and user story generation.
    """

    agent_type = AgentType.BA
    agent_name = "Business Analyst Agent"
    agent_description = "Expert in requirements elicitation and user story creation"
    capabilities = [
        "REQUIREMENTS_ELICITATION",
        "USER_STORY_GENERATION",
        "ACCEPTANCE_CRITERIA",
        "STORY_ESTIMATION",
        "EPIC_BREAKDOWN"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a BA task.

        Expected input_data:
            - task_type: ELICIT_REQUIREMENTS | GENERATE_STORIES | ESTIMATE | BREAKDOWN_EPIC
            - idea: Project/feature idea
            - existing_requirements: (optional) Existing requirements
            - context: (optional) Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'GENERATE_STORIES')
        idea = input_data.get('idea', '')
        existing_requirements = input_data.get('existing_requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing BA task: {task_type}")

        if task_type == 'ELICIT_REQUIREMENTS':
            return self._elicit_requirements(idea, context)
        elif task_type == 'GENERATE_STORIES':
            return self._generate_user_stories(idea, existing_requirements, context)
        elif task_type == 'ESTIMATE':
            return self._estimate_stories(input_data.get('stories', []))
        elif task_type == 'BREAKDOWN_EPIC':
            return self._breakdown_epic(idea, context)
        else:
            raise ValueError(f"Unknown BA task type: {task_type}")

    def _elicit_requirements(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Elicit requirements from a high-level idea."""

        user_message = f"""
I have the following project/feature idea:

{idea}

Context: {context if context else 'None'}

Please help me elicit comprehensive requirements by:

1. **Understanding the Problem**
   - What problem are we solving?
   - Who are the users?
   - What are the business goals?

2. **Functional Requirements**
   - What features are needed?
   - What should the system do?
   - What are the user workflows?

3. **Non-Functional Requirements**
   - Performance requirements
   - Security requirements
   - Scalability requirements
   - Usability requirements

4. **Constraints and Assumptions**
   - Technical constraints
   - Business constraints
   - Key assumptions

5. **Success Criteria**
   - How will we measure success?
   - What are the KPIs?

Please be thorough and ask clarifying questions if needed.
"""

        response = self.generate_response(user_message, context)

        return {
            'requirements': response,
            'idea': idea,
            'needs_clarification': self._check_needs_clarification(response)
        }

    def _generate_user_stories(
        self,
        idea: str,
        existing_requirements: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate user stories from idea/requirements."""

        user_message = f"""
I need you to generate comprehensive user stories for the following project:

Project Idea:
{idea}

{f"Existing Requirements:\n{existing_requirements}\n" if existing_requirements else ""}

Context: {context if context else 'None'}

Please generate user stories following this format:

**Epic**: [Epic Name]

**Story**: As a [user type], I want [goal] so that [benefit]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Technical Notes**:
- Implementation considerations
- Dependencies
- Risks

**Story Points**: [Estimated points 1-13 Fibonacci]

Please:
1. Group stories into logical Epics
2. Cover all major features
3. Include edge cases
4. Prioritize stories (Must Have, Should Have, Could Have)
5. Estimate story points
6. Identify dependencies between stories
"""

        response = self.generate_response(user_message, context)

        stories = self._parse_stories(response)

        return {
            'stories': stories,
            'raw_output': response,
            'total_stories': len(stories)
        }

    def _estimate_stories(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate story points for given stories."""

        stories_text = "\n\n".join([
            f"**Story {i+1}**: {story.get('title', story.get('description', ''))}"
            for i, story in enumerate(stories)
        ])

        user_message = f"""
Please estimate the following user stories using Fibonacci scale (1, 2, 3, 5, 8, 13):

{stories_text}

For each story, provide:
1. Story Points (Fibonacci: 1, 2, 3, 5, 8, 13)
2. Reasoning for the estimate
3. Risk factors
4. Assumptions

Consider:
- Complexity
- Uncertainty
- Amount of work
- Dependencies
"""

        response = self.generate_response(user_message)

        return {
            'estimates': response,
            'stories_count': len(stories)
        }

    def _breakdown_epic(self, epic: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Break down an epic into smaller stories."""

        user_message = f"""
Please break down this epic into smaller, actionable user stories:

Epic:
{epic}

Context: {context if context else 'None'}

For each story:
1. Clear title
2. User story format (As a... I want... So that...)
3. Acceptance criteria
4. Story points estimate
5. Priority

Ensure stories are:
- Small enough to complete in 1 sprint
- Independent (where possible)
- Testable
- Valuable
"""

        response = self.generate_response(user_message, context)

        stories = self._parse_stories(response)

        return {
            'epic': epic,
            'stories': stories,
            'raw_output': response,
            'total_stories': len(stories)
        }

    def _parse_stories(self, response: str) -> List[Dict[str, Any]]:
        """Parse user stories from the response text."""
        stories = []
        current_story = {}

        lines = response.split('\n')
        for line in lines:
            line = line.strip()

            if line.startswith('**Story'):
                if current_story:
                    stories.append(current_story)
                current_story = {'description': line}
            elif line.startswith('**Epic'):
                if current_story:
                    current_story['epic'] = line.replace('**Epic**:', '').strip()
            elif line.startswith('**Story Points'):
                if current_story:
                    current_story['story_points'] = line.replace('**Story Points**:', '').strip()
            elif line.startswith('**Acceptance Criteria'):
                current_story['has_acceptance_criteria'] = True

        if current_story:
            stories.append(current_story)

        return stories

    def _check_needs_clarification(self, response: str) -> bool:
        """Check if the requirements need clarification."""
        clarification_indicators = [
            'need clarification',
            'unclear',
            'ambiguous',
            'please provide',
            'could you clarify',
            'more information needed'
        ]

        response_lower = response.lower()
        return any(indicator in response_lower for indicator in clarification_indicators)
