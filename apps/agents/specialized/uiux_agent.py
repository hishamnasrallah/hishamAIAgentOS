from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class UIUXAgent(BaseAgent):
    """
    UI/UX Designer Agent
    Specialized in user interface design and user experience optimization.
    """

    agent_type = AgentType.UI_UX
    agent_name = "UI/UX Agent"
    agent_description = "Expert in user interface design and user experience"
    capabilities = [
        "UI_DESIGN",
        "UX_ANALYSIS",
        "WIREFRAME_CREATION",
        "USER_FLOW_DESIGN",
        "ACCESSIBILITY_AUDIT"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a UI/UX task.

        Expected input_data:
            - task_type: DESIGN | ANALYZE | WIREFRAME | USER_FLOW | ACCESSIBILITY
            - feature: Feature to design
            - requirements: Requirements
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'DESIGN')
        feature = input_data.get('feature', '')
        requirements = input_data.get('requirements', '')
        context = input_data.get('context', {})

        logger.info(f"Executing UI/UX task: {task_type}")

        user_message = self._build_uiux_prompt(task_type, feature, requirements, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'feature': feature
        }

    def _build_uiux_prompt(
        self,
        task_type: str,
        feature: str,
        requirements: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for UI/UX task."""

        if task_type == 'DESIGN':
            return f"""
I need you to design the UI for this feature.

Feature:
{feature}

Requirements:
{requirements}

Please provide comprehensive UI design:

1. **Design System** 🎨
   - Color palette
   - Typography
   - Spacing system
   - Component library

2. **Layout Design** 📐
   - Screen layout description
   - Grid system
   - Responsive breakpoints
   - Component placement

3. **Component Design** 🧩
   For each major component:
   - Visual description
   - States (default, hover, active, disabled)
   - Interactions
   - Animations

4. **Visual Hierarchy** 👁️
   - Primary actions
   - Secondary actions
   - Information hierarchy
   - Focus areas

5. **Micro-interactions** ✨
   - Button animations
   - Loading states
   - Transitions
   - Feedback mechanisms

6. **Design Rationale** 💡
   - Why these design choices?
   - How does it meet user needs?
   - Design principles applied

7. **HTML/CSS Structure** 💻
   - Semantic HTML structure
   - Tailwind CSS classes
   - Component hierarchy

Context: {context if context else 'None'}
"""

        elif task_type == 'ANALYZE':
            return f"""
I need you to analyze the UX of this feature.

Feature:
{feature}

Details:
{requirements}

Please provide comprehensive UX analysis:

1. **User Journey Analysis** 🗺️
   - Current user flow
   - Pain points
   - Friction areas
   - Drop-off points

2. **Usability Assessment** 📊
   - Ease of use (1-10)
   - Learnability
   - Efficiency
   - Error prevention
   - Satisfaction

3. **Information Architecture** 🏗️
   - Content organization
   - Navigation clarity
   - Mental model alignment
   - Findability

4. **Interaction Design** 🖱️
   - Interaction patterns
   - Feedback quality
   - Response times
   - Error handling

5. **Visual Design** 🎨
   - Visual hierarchy
   - Consistency
   - Aesthetics
   - Brand alignment

6. **Accessibility** ♿
   - WCAG compliance
   - Keyboard navigation
   - Screen reader support
   - Color contrast

7. **Issues Identified** 🚨
   For each issue:
   - Severity (Critical/High/Medium/Low)
   - Impact on users
   - Recommended fix

8. **Improvement Recommendations** 💡
   - Quick wins
   - Major improvements
   - Long-term enhancements

Context: {context if context else 'None'}
"""

        elif task_type == 'WIREFRAME':
            return f"""
I need wireframes for this feature.

Feature:
{feature}

Requirements:
{requirements}

Please provide detailed wireframe descriptions:

1. **Screen Overview** 📱
   - Screen purpose
   - Key elements
   - User goals

2. **Layout Structure** 📐
   Describe the wireframe using ASCII art or detailed description:

   ```
   +----------------------------------+
   | Header                            |
   +----------------------------------+
   | Navigation                        |
   +----------------------------------+
   |  Sidebar  |  Main Content        |
   |           |                      |
   |           |                      |
   +----------------------------------+
   | Footer                            |
   +----------------------------------+
   ```

3. **Component Breakdown** 🧩
   For each component:
   - Component name
   - Position
   - Size/Dimensions
   - Content
   - Interactions

4. **Element Details** 📝
   - Headers (H1, H2, etc.)
   - Buttons (primary, secondary)
   - Forms (inputs, labels)
   - Images/Icons
   - Lists
   - Cards

5. **Responsive Behavior** 📱💻
   - Mobile (< 768px)
   - Tablet (768px - 1024px)
   - Desktop (> 1024px)

6. **Interactive Elements** 🔄
   - Click actions
   - Hover states
   - Loading states
   - Error states

Context: {context if context else 'None'}
"""

        elif task_type == 'USER_FLOW':
            return f"""
I need you to design the user flow.

Feature:
{feature}

Requirements:
{requirements}

Please provide comprehensive user flow design:

1. **User Flow Diagram** 🗺️
   Describe the flow:

   ```
   [Start] → [Step 1] → [Decision?]
                           ↓ Yes      ↓ No
                      [Step 2A]   [Step 2B]
                           ↓           ↓
                       [Success]   [Error]
   ```

2. **Flow Steps** 📋
   For each step:
   - Step number
   - User action
   - System response
   - Decision points
   - Alternative paths

3. **Happy Path** ✅
   - Ideal user journey
   - Minimal steps
   - Success outcome

4. **Alternative Paths** 🔀
   - Edge cases
   - Error scenarios
   - Recovery paths

5. **Entry Points** 🚪
   - How users start the flow
   - Context
   - Prerequisites

6. **Exit Points** 🚶
   - Success states
   - Failure states
   - Abandon points

7. **Interaction Details** 🖱️
   - Form inputs
   - Button clicks
   - Validations
   - Feedback messages

8. **Optimization Opportunities** 💡
   - Steps to reduce
   - Friction to remove
   - Clarity to improve

Context: {context if context else 'None'}
"""

        elif task_type == 'ACCESSIBILITY':
            return f"""
I need an accessibility audit.

Feature:
{feature}

{f"Details:\n{requirements}\n" if requirements else ""}

Please provide comprehensive accessibility audit:

1. **WCAG 2.1 Compliance** ♿

   **Level A Requirements**:
   - [ ] Keyboard accessible
   - [ ] Text alternatives
   - [ ] Time-based media
   - Findings:

   **Level AA Requirements**:
   - [ ] Color contrast (4.5:1)
   - [ ] Resize text (200%)
   - [ ] Multiple ways to navigate
   - Findings:

   **Level AAA Requirements** (optional):
   - [ ] Color contrast (7:1)
   - [ ] Sign language
   - Findings:

2. **Keyboard Navigation** ⌨️
   - Tab order logical?
   - All interactive elements reachable?
   - Focus indicators visible?
   - Keyboard shortcuts?
   - Findings:

3. **Screen Reader Support** 🔊
   - Semantic HTML used?
   - ARIA labels present?
   - Landmark regions?
   - Alt text for images?
   - Findings:

4. **Visual Accessibility** 👁️
   - Color contrast ratios
   - Text size
   - Line height
   - Font readability
   - Findings:

5. **Motor Accessibility** 🖱️
   - Click target size (44x44px min)
   - Spacing between targets
   - No time limits (or adjustable)
   - Findings:

6. **Cognitive Accessibility** 🧠
   - Clear language
   - Consistent navigation
   - Error prevention
   - Help available
   - Findings:

7. **Issues Found** 🚨
   For each issue:
   - Severity (Critical/High/Medium/Low)
   - WCAG criterion violated
   - Impact on users
   - How to fix

8. **Recommendations** 💡
   - Priority fixes
   - Implementation guidance
   - Testing approach

Context: {context if context else 'None'}
"""

        else:
            return requirements
