from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class CodeReviewAgent(BaseAgent):
    """
    FAANG-level Code Reviewer Agent
    Provides strict, comprehensive code reviews.
    """

    agent_type = AgentType.CODE_REVIEW
    agent_name = "Code Review Agent"
    agent_description = "Strict FAANG-level code reviewer"
    capabilities = [
        "CODE_REVIEW",
        "SECURITY_AUDIT",
        "PERFORMANCE_ANALYSIS",
        "BEST_PRACTICES_CHECK"
    ]

    REVIEW_PILLARS = [
        'Correctness',
        'Performance',
        'Security',
        'Maintainability',
        'Readability',
        'Testability',
        'Error Handling',
        'Documentation',
        'Best Practices',
        'Scalability'
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a code review task.

        Expected input_data:
            - code: Code to review
            - language: Programming language
            - context: (optional) Additional context
            - focus_areas: (optional) Specific areas to focus on
        """
        input_data = task.input_data
        code = input_data.get('code', '')
        language = input_data.get('language', 'Python')
        context = input_data.get('context', {})
        focus_areas = input_data.get('focus_areas', self.REVIEW_PILLARS)

        logger.info(f"Executing code review for {language} code")

        user_message = self._build_review_prompt(code, language, focus_areas, context)

        response = self.generate_response(
            user_message,
            context={'language': language, 'focus_areas': focus_areas}
        )

        return {
            'review': response,
            'language': language,
            'focus_areas': focus_areas,
            'scores': self._extract_scores(response)
        }

    def _build_review_prompt(
        self,
        code: str,
        language: str,
        focus_areas: list,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for code review."""

        return f"""
Please perform a comprehensive code review of the following {language} code.

Code to Review:
```{language.lower()}
{code}
```

Focus Areas: {', '.join(focus_areas)}

Additional Context: {context if context else 'None'}

Please provide:

1. **Overall Score** (0-10 scale)
2. **Detailed Scores** for each pillar:
   - Correctness (Does it work? Edge cases handled?)
   - Performance (Efficient algorithms? No N+1 queries?)
   - Security (SQL injection? XSS? Secure secrets?)
   - Maintainability (Easy to modify and extend?)
   - Readability (Clear naming? Good structure?)
   - Testability (Easy to test? Low coupling?)
   - Error Handling (Proper exception handling?)
   - Documentation (Adequate documentation?)
   - Best Practices (SOLID? DRY? Design patterns?)
   - Scalability (Handles increased load?)

3. **Critical Issues** (MUST FIX)
4. **Major Issues** (SHOULD FIX)
5. **Minor Issues** (NICE TO HAVE)
6. **Positive Aspects**
7. **Recommended Actions** (prioritized)

Be strict but constructive. Provide concrete examples and explain the "why" behind each issue.
"""

    def _extract_scores(self, response: str) -> Dict[str, float]:
        """Extract numerical scores from the review response."""
        scores = {}
        try:
            for line in response.split('\n'):
                for pillar in self.REVIEW_PILLARS:
                    if pillar.lower() in line.lower() and '/10' in line:
                        score_str = line.split('/10')[0].strip().split()[-1]
                        try:
                            scores[pillar] = float(score_str)
                        except ValueError:
                            pass
        except Exception as e:
            logger.warning(f"Could not extract scores: {str(e)}")

        return scores
