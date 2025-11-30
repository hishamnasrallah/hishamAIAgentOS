from typing import Dict, Any, List
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class QAAgent(BaseAgent):
    """
    QA Engineer Agent
    Specialized in test planning, test case creation, and quality assurance.
    """

    agent_type = AgentType.QA
    agent_name = "QA Agent"
    agent_description = "Expert in testing, quality assurance, and test automation"
    capabilities = [
        "TEST_PLAN_CREATION",
        "TEST_CASE_GENERATION",
        "BUG_IDENTIFICATION",
        "TEST_AUTOMATION",
        "QUALITY_METRICS"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a QA task.

        Expected input_data:
            - task_type: TEST_PLAN | TEST_CASES | BUG_REPORT | AUTOMATION | REVIEW
            - feature: Feature to test
            - requirements: Requirements
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'TEST_CASES')
        feature = input_data.get('feature', '')
        requirements = input_data.get('requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing QA task: {task_type}")

        user_message = self._build_qa_prompt(task_type, feature, requirements, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'feature': feature,
            'test_cases': self._extract_test_cases(response) if task_type == 'TEST_CASES' else []
        }

    def _build_qa_prompt(
        self,
        task_type: str,
        feature: str,
        requirements: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for QA task."""

        if task_type == 'TEST_PLAN':
            return f"""
I need you to create a comprehensive test plan for the following feature:

Feature:
{feature}

Requirements:
{requirements}

Please provide:
1. **Test Strategy**
   - Testing approach
   - Test levels (unit, integration, system, acceptance)
   - Testing types (functional, performance, security, etc.)

2. **Test Scope**
   - In scope
   - Out of scope

3. **Test Cases Summary**
   - Positive scenarios
   - Negative scenarios
   - Edge cases
   - Performance test cases
   - Security test cases

4. **Test Environment**
   - Required test environments
   - Test data needs

5. **Entry & Exit Criteria**

6. **Risk Analysis**

Context: {context if context else 'None'}
"""

        elif task_type == 'TEST_CASES':
            return f"""
I need you to generate detailed test cases for the following feature:

Feature:
{feature}

Requirements:
{requirements}

For each test case, provide:
1. **Test Case ID**: TC_XXX
2. **Test Case Title**: Clear, descriptive title
3. **Priority**: High/Medium/Low
4. **Preconditions**: Setup required
5. **Test Steps**: Numbered steps
6. **Expected Result**: What should happen
7. **Test Data**: Sample data needed
8. **Type**: Positive/Negative/Edge Case

Please include:
- Happy path scenarios
- Negative scenarios
- Boundary value tests
- Edge cases
- Integration scenarios

Context: {context if context else 'None'}
"""

        elif task_type == 'BUG_REPORT':
            return f"""
I need help analyzing and reporting a bug:

Issue:
{requirements}

Feature Context:
{feature}

Please provide a comprehensive bug report:

1. **Bug Summary**: One-line description

2. **Severity**: Critical/High/Medium/Low

3. **Priority**: P0/P1/P2/P3

4. **Steps to Reproduce**:
   - Step 1
   - Step 2
   - ...

5. **Expected Behavior**: What should happen

6. **Actual Behavior**: What is happening

7. **Root Cause Analysis**: Why is this happening?

8. **Affected Areas**: What else might be impacted?

9. **Suggested Fix**: How to fix it

10. **Test Cases**: How to verify the fix

Context: {context if context else 'None'}
"""

        elif task_type == 'AUTOMATION':
            return f"""
I need you to create test automation code.

Feature:
{feature}

Requirements:
{requirements}

Please provide:
1. Test automation framework choice
2. Test automation code
3. Test data setup
4. Assertions
5. Clean up steps
6. Comments explaining the tests

Context: {context if context else 'None'}
"""

        elif task_type == 'REVIEW':
            return f"""
I need you to review the quality of this feature:

Feature:
{feature}

Details:
{requirements}

Please provide:
1. Quality assessment
2. Test coverage analysis
3. Identified gaps
4. Risk areas
5. Recommendations for improvement

Context: {context if context else 'None'}
"""

        else:
            return requirements

    def _extract_test_cases(self, response: str) -> List[Dict[str, Any]]:
        """Extract test cases from the response."""
        test_cases = []
        current_case = {}

        lines = response.split('\n')
        for line in lines:
            line = line.strip()

            if line.startswith('**Test Case ID'):
                if current_case:
                    test_cases.append(current_case)
                current_case = {'id': line.split(':')[-1].strip()}
            elif line.startswith('**Test Case Title'):
                current_case['title'] = line.split(':')[-1].strip()
            elif line.startswith('**Priority'):
                current_case['priority'] = line.split(':')[-1].strip()

        if current_case:
            test_cases.append(current_case)

        return test_cases
