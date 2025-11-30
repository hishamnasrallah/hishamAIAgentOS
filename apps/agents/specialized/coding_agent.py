from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class CodingAgent(BaseAgent):
    """
    Expert Software Developer Agent
    Specialized in writing, modifying, and improving code.
    """

    agent_type = AgentType.CODING
    agent_name = "Coding Agent"
    agent_description = "Expert software developer for writing and modifying code"
    capabilities = [
        "CODE_GENERATION",
        "CODE_MODIFICATION",
        "REFACTORING",
        "DEBUGGING",
        "CODE_EXPLANATION"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a coding task.

        Expected input_data:
            - task_type: NEW_BUILD | MODIFY_EXISTING | REFACTOR | DEBUG
            - language: Programming language
            - requirements: Task requirements
            - existing_code: (optional) Existing code to modify
            - context: (optional) Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'NEW_BUILD')
        language = input_data.get('language', 'Python')
        requirements = input_data.get('requirements', '')
        existing_code = input_data.get('existing_code', '')
        context = input_data.get('context', {})

        logger.info(f"Executing coding task: {task_type} in {language}")

        prompt_context = {
            'task_type': task_type,
            'language': language,
            'requirements': requirements,
        }

        if existing_code:
            prompt_context['existing_code'] = existing_code

        user_message = self._build_coding_prompt(
            task_type, language, requirements, existing_code, context
        )

        response = self.generate_response(user_message, context=prompt_context)

        return {
            'code': response,
            'language': language,
            'task_type': task_type,
            'agent_notes': self._extract_notes(response)
        }

    def _build_coding_prompt(
        self,
        task_type: str,
        language: str,
        requirements: str,
        existing_code: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for the coding task."""

        if task_type == 'NEW_BUILD':
            return f"""
I need you to write new code in {language}.

Requirements:
{requirements}

Please provide:
1. Complete, production-ready code
2. Proper error handling
3. Clear documentation
4. Following best practices for {language}

Context: {context if context else 'None'}
"""

        elif task_type == 'MODIFY_EXISTING':
            return f"""
I need you to modify existing code in {language}.

Requirements:
{requirements}

Existing Code:
```{language.lower()}
{existing_code}
```

Please:
1. Make the requested modifications
2. Maintain existing code style
3. Add comments on modified lines with # MODIFIED
4. Explain the changes

Context: {context if context else 'None'}
"""

        elif task_type == 'REFACTOR':
            return f"""
I need you to refactor this code in {language}.

Goals:
{requirements}

Code to Refactor:
```{language.lower()}
{existing_code}
```

Please:
1. Improve code quality
2. Follow SOLID principles
3. Enhance readability and maintainability
4. Explain key changes

Context: {context if context else 'None'}
"""

        elif task_type == 'DEBUG':
            return f"""
I need you to debug and fix issues in this code in {language}.

Problem Description:
{requirements}

Code with Issues:
```{language.lower()}
{existing_code}
```

Please:
1. Identify the bugs
2. Provide fixed code
3. Explain what was wrong
4. Suggest preventive measures

Context: {context if context else 'None'}
"""

        else:
            return requirements

    def _extract_notes(self, response: str) -> str:
        """Extract agent notes from the response."""
        if "## 💡 Improvements Needed" in response:
            return response.split("## 💡 Improvements Needed")[1].split("##")[0].strip()
        return ""
