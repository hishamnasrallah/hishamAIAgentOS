from typing import Dict, Any, List
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class SecurityAgent(BaseAgent):
    """
    Security Agent
    Specialized in security audits, vulnerability detection, and secure coding practices.
    """

    agent_type = AgentType.SECURITY
    agent_name = "Security Agent"
    agent_description = "Expert in security analysis and vulnerability detection"
    capabilities = [
        "SECURITY_AUDIT",
        "VULNERABILITY_DETECTION",
        "THREAT_MODELING",
        "SECURE_CODE_REVIEW",
        "PENETRATION_TESTING"
    ]

    OWASP_TOP_10 = [
        "Broken Access Control",
        "Cryptographic Failures",
        "Injection",
        "Insecure Design",
        "Security Misconfiguration",
        "Vulnerable and Outdated Components",
        "Identification and Authentication Failures",
        "Software and Data Integrity Failures",
        "Security Logging and Monitoring Failures",
        "Server-Side Request Forgery (SSRF)"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Security task.

        Expected input_data:
            - task_type: AUDIT | VULN_SCAN | THREAT_MODEL | CODE_REVIEW | PENTEST
            - code: (optional) Code to review
            - system: System description
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'AUDIT')
        code = input_data.get('code', '')
        system = input_data.get('system', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Security task: {task_type}")

        user_message = self._build_security_prompt(task_type, code, system, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'vulnerabilities': self._extract_vulnerabilities(response)
        }

    def _build_security_prompt(
        self,
        task_type: str,
        code: str,
        system: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for security task."""

        if task_type == 'AUDIT':
            return f"""
I need you to perform a comprehensive security audit.

System Description:
{system}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please perform security audit based on OWASP Top 10:

**OWASP Top 10 Analysis:**

1. **Broken Access Control** 🔐
   - Authorization checks
   - Privilege escalation risks
   - Findings:

2. **Cryptographic Failures** 🔒
   - Encryption usage
   - Key management
   - Findings:

3. **Injection** 💉
   - SQL injection
   - Command injection
   - XSS vulnerabilities
   - Findings:

4. **Insecure Design** 🏗️
   - Security by design
   - Threat modeling
   - Findings:

5. **Security Misconfiguration** ⚙️
   - Default configurations
   - Unnecessary features
   - Findings:

6. **Vulnerable Components** 📦
   - Outdated dependencies
   - Known vulnerabilities
   - Findings:

7. **Authentication Failures** 🎫
   - Authentication mechanisms
   - Session management
   - Findings:

8. **Data Integrity Failures** 📝
   - Data validation
   - Integrity checks
   - Findings:

9. **Logging & Monitoring** 📊
   - Security logging
   - Incident detection
   - Findings:

10. **SSRF** 🌐
    - External requests
    - URL validation
    - Findings:

**Overall Security Score**: X/10

**Critical Issues**: List with severity HIGH

**Recommendations**: Prioritized action items

Context: {context if context else 'None'}
"""

        elif task_type == 'VULN_SCAN':
            return f"""
I need you to scan for vulnerabilities.

{f"Code:\n```\n{code}\n```\n" if code else ""}

System:
{system}

Please identify:

1. **Code Vulnerabilities** 🐛
   - Security bugs
   - Insecure patterns
   - Dangerous functions

2. **Input Validation Issues** ✅
   - Missing validation
   - Improper sanitization
   - Type confusion

3. **Authentication Issues** 🔑
   - Weak authentication
   - Session management flaws
   - Password handling

4. **Authorization Issues** 🚪
   - Missing authorization checks
   - Privilege escalation
   - IDOR vulnerabilities

5. **Data Exposure** 📢
   - Sensitive data leaks
   - Improper error messages
   - Debug information

6. **Cryptography Issues** 🔐
   - Weak algorithms
   - Hardcoded secrets
   - Improper key management

For each vulnerability:
- **Severity**: Critical/High/Medium/Low
- **Description**: What is it?
- **Impact**: What can happen?
- **PoC**: How to exploit
- **Fix**: How to remediate
- **CWE ID**: Common Weakness Enumeration

Context: {context if context else 'None'}
"""

        elif task_type == 'THREAT_MODEL':
            return f"""
I need you to create a threat model.

System Description:
{system}

Please provide comprehensive threat modeling:

1. **System Architecture** 🏗️
   - Components
   - Data flows
   - Trust boundaries
   - Entry points

2. **Assets** 💎
   - What needs protection?
   - Value of each asset
   - Impact if compromised

3. **Threat Identification** (STRIDE)
   - **S**poofing: Identity spoofing threats
   - **T**ampering: Data tampering threats
   - **R**epudiation: Non-repudiation issues
   - **I**nformation Disclosure: Data exposure
   - **D**enial of Service: Availability threats
   - **E**levation of Privilege: Authorization bypass

4. **Risk Assessment**
   For each threat:
   - Likelihood (High/Medium/Low)
   - Impact (High/Medium/Low)
   - Risk Score

5. **Mitigation Strategies** 🛡️
   - Controls to implement
   - Secure design patterns
   - Defense in depth

6. **Attack Scenarios** ⚔️
   - Most likely attacks
   - Attack paths
   - Attack chains

Context: {context if context else 'None'}
"""

        elif task_type == 'CODE_REVIEW':
            return f"""
I need a security-focused code review.

Code:
```
{code}
```

Please review for:

1. **Input Validation** ✅
   - All inputs validated?
   - Proper sanitization?
   - Type checking?

2. **Output Encoding** 📤
   - XSS prevention
   - Proper encoding
   - Context-aware escaping

3. **Authentication** 🔑
   - Secure authentication
   - Password handling
   - Session management

4. **Authorization** 🚪
   - Access controls
   - Least privilege
   - Role checks

5. **Cryptography** 🔐
   - Strong algorithms
   - Proper key management
   - No hardcoded secrets

6. **Error Handling** ⚠️
   - Safe error messages
   - No information leakage
   - Proper logging

7. **Database Security** 🗄️
   - Parameterized queries
   - No SQL injection
   - Least privilege DB access

8. **API Security** 🔌
   - Rate limiting
   - Input validation
   - Authentication/Authorization

**Security Score**: X/10

**Critical Issues**: Must fix

**Recommendations**: Step-by-step fixes

Context: {context if context else 'None'}
"""

        elif task_type == 'PENTEST':
            return f"""
I need a penetration testing plan.

System:
{system}

{f"Code:\n```\n{code}\n```\n" if code else ""}

Please provide:

1. **Scope Definition** 🎯
   - What to test
   - What not to test
   - Rules of engagement

2. **Test Approach** 🔍
   - Reconnaissance
   - Vulnerability analysis
   - Exploitation
   - Post-exploitation
   - Reporting

3. **Test Cases** ✅
   - Authentication bypass
   - Authorization flaws
   - Injection attacks
   - Business logic flaws
   - API security

4. **Tools & Techniques** 🛠️
   - Recommended tools
   - Manual testing approach
   - Automation scripts

5. **Expected Findings** 📋
   - Common vulnerabilities
   - Areas of concern
   - Risk assessment

6. **Remediation Guidance** 💡
   - How to fix issues
   - Best practices
   - Security hardening

Context: {context if context else 'None'}
"""

        else:
            return system or code

    def _extract_vulnerabilities(self, response: str) -> List[Dict[str, Any]]:
        """Extract vulnerabilities from response."""
        vulnerabilities = []
        current_vuln = {}

        lines = response.split('\n')
        for line in lines:
            line = line.strip()

            if '**Severity**:' in line or '**severity**:' in line:
                if current_vuln:
                    vulnerabilities.append(current_vuln)
                current_vuln = {'severity': line.split(':')[-1].strip()}
            elif '**Description**:' in line:
                current_vuln['description'] = line.split(':')[-1].strip()
            elif '**Impact**:' in line:
                current_vuln['impact'] = line.split(':')[-1].strip()

        if current_vuln:
            vulnerabilities.append(current_vuln)

        return vulnerabilities
