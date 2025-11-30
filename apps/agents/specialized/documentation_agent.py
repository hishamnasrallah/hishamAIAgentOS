from typing import Dict, Any
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class DocumentationAgent(BaseAgent):
    """
    Documentation Specialist Agent
    Specialized in creating comprehensive technical documentation.
    """

    agent_type = AgentType.DOCUMENTATION
    agent_name = "Documentation Agent"
    agent_description = "Expert in technical writing and documentation"
    capabilities = [
        "CODE_DOCUMENTATION",
        "API_DOCUMENTATION",
        "USER_GUIDES",
        "TECHNICAL_SPECS",
        "README_CREATION"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Documentation task.

        Expected input_data:
            - task_type: CODE_DOCS | API_DOCS | USER_GUIDE | TECH_SPEC | README
            - code: (optional) Code to document
            - system: System description
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'CODE_DOCS')
        code = input_data.get('code', '')
        system = input_data.get('system', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Documentation task: {task_type}")

        user_message = self._build_docs_prompt(task_type, code, system, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'documentation': response
        }

    def _build_docs_prompt(
        self,
        task_type: str,
        code: str,
        system: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for documentation task."""

        if task_type == 'CODE_DOCS':
            return f"""
I need you to create comprehensive code documentation.

Code:
```
{code}
```

Please provide:

1. **Overview** 📋
   - What does this code do?
   - Purpose and responsibilities
   - Key functionality

2. **Function/Method Documentation** 📝
   For each function:
   - Purpose
   - Parameters (type, description)
   - Return value (type, description)
   - Exceptions/Errors
   - Examples

3. **Class Documentation** 🏗️
   For each class:
   - Purpose and responsibility
   - Attributes
   - Methods overview
   - Usage examples
   - Design patterns used

4. **Complex Logic Explanation** 🧠
   - Algorithm explanations
   - Why certain approaches were chosen
   - Edge cases handled

5. **Dependencies** 🔗
   - External libraries
   - Internal modules
   - System requirements

6. **Usage Examples** 💡
   - Basic usage
   - Advanced usage
   - Common patterns

Context: {context if context else 'None'}
"""

        elif task_type == 'API_DOCS':
            return f"""
I need comprehensive API documentation.

API Details:
{system}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please provide:

1. **API Overview** 📋
   - Purpose
   - Base URL
   - Authentication
   - Rate limiting

2. **Endpoints** 🔌
   For each endpoint:

   ### `METHOD /endpoint/path`

   **Description**: What it does

   **Authentication**: Required/Optional

   **Parameters**:
   - Path parameters
   - Query parameters
   - Body parameters

   **Request Example**:
   ```json
   {
     "example": "request"
   }
   ```

   **Response** (200 OK):
   ```json
   {
     "example": "response"
   }
   ```

   **Error Responses**:
   - 400: Bad Request
   - 401: Unauthorized
   - 404: Not Found
   - 500: Server Error

3. **Data Models** 📊
   - Object schemas
   - Field descriptions
   - Validation rules

4. **Authentication** 🔐
   - How to authenticate
   - Token format
   - Token refresh

5. **Error Handling** ⚠️
   - Error format
   - Error codes
   - Error messages

6. **Code Examples** 💻
   - cURL examples
   - Python examples
   - JavaScript examples

Context: {context if context else 'None'}
"""

        elif task_type == 'USER_GUIDE':
            return f"""
I need you to create a user guide.

System:
{system}

Please create a comprehensive user guide:

1. **Introduction** 👋
   - What is this system?
   - Who is it for?
   - Key features

2. **Getting Started** 🚀
   - Installation/Setup
   - Initial configuration
   - First steps

3. **Feature Guides** 📚
   For each major feature:
   - What it does
   - How to use it
   - Step-by-step instructions
   - Screenshots/Visuals (describe what should be shown)
   - Tips and best practices

4. **Common Tasks** ✅
   - Task 1: Step-by-step
   - Task 2: Step-by-step
   - Task 3: Step-by-step

5. **Troubleshooting** 🔧
   - Common issues
   - Solutions
   - Where to get help

6. **FAQ** ❓
   - Frequently asked questions
   - Clear, concise answers

7. **Glossary** 📖
   - Technical terms explained
   - Key concepts

Context: {context if context else 'None'}
"""

        elif task_type == 'TECH_SPEC':
            return f"""
I need you to create a technical specification document.

System:
{system}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please provide:

1. **Executive Summary** 📋
   - Overview
   - Objectives
   - Scope

2. **System Architecture** 🏗️
   - High-level architecture
   - Components
   - Technologies used
   - Integration points

3. **Functional Requirements** ⚙️
   - Feature 1: Detailed spec
   - Feature 2: Detailed spec
   - Feature 3: Detailed spec

4. **Non-Functional Requirements** 📊
   - Performance requirements
   - Security requirements
   - Scalability requirements
   - Reliability requirements

5. **Data Model** 🗄️
   - Database schema
   - Entity relationships
   - Data flows

6. **API Specification** 🔌
   - Endpoints
   - Request/Response formats
   - Authentication

7. **Security Considerations** 🔐
   - Authentication/Authorization
   - Data protection
   - Security measures

8. **Deployment** 🚀
   - Infrastructure requirements
   - Deployment process
   - Environment configuration

9. **Testing Strategy** ✅
   - Unit testing
   - Integration testing
   - Performance testing

10. **Future Considerations** 🔮
    - Scalability path
    - Feature roadmap
    - Technical debt

Context: {context if context else 'None'}
"""

        elif task_type == 'README':
            return f"""
I need you to create an excellent README.md file.

Project:
{system}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please create a comprehensive README:

# Project Name

## 📋 Overview
Brief description of what this project does and why it exists.

## ✨ Features
- Feature 1
- Feature 2
- Feature 3

## 🚀 Quick Start

### Prerequisites
- Requirement 1
- Requirement 2

### Installation
```bash
# Installation steps
```

### Usage
```bash
# Basic usage examples
```

## 📖 Documentation
Links to detailed documentation

## 🏗️ Architecture
High-level overview of the system architecture

## 🛠️ Development

### Setup
Development environment setup

### Running Tests
```bash
# Test commands
```

### Building
```bash
# Build commands
```

## 🤝 Contributing
How to contribute to the project

## 📝 License
License information

## 🙏 Acknowledgments
Credits and thanks

## 📧 Contact
How to reach the maintainers

Context: {context if context else 'None'}
"""

        else:
            return system or code
