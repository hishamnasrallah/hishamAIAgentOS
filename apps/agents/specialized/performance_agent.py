from typing import Dict, Any, List
from apps.agents.base_agent import BaseAgent
from apps.agents.models import AgentTask, AgentType
import logging

logger = logging.getLogger(__name__)


class PerformanceAgent(BaseAgent):
    """
    Performance Optimization Agent
    Specialized in performance analysis, bottleneck identification, and optimization.
    """

    agent_type = AgentType.PERFORMANCE
    agent_name = "Performance Agent"
    agent_description = "Expert in performance optimization and scalability"
    capabilities = [
        "PERFORMANCE_ANALYSIS",
        "BOTTLENECK_IDENTIFICATION",
        "OPTIMIZATION_RECOMMENDATIONS",
        "LOAD_TESTING",
        "SCALABILITY_ASSESSMENT"
    ]

    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """
        Execute a Performance task.

        Expected input_data:
            - task_type: ANALYZE | OPTIMIZE | LOAD_TEST | SCALE | PROFILE
            - code: (optional) Code to analyze
            - metrics: (optional) Performance metrics
            - system: System description
            - context: Additional context
        """
        input_data = task.input_data
        task_type = input_data.get('task_type', 'ANALYZE')
        code = input_data.get('code', '')
        metrics = input_data.get('metrics', {})
        system = input_data.get('system', '')
        context = input_data.get('context', {})

        logger.info(f"Executing Performance task: {task_type}")

        user_message = self._build_performance_prompt(task_type, code, metrics, system, context)

        response = self.generate_response(user_message, context)

        return {
            'output': response,
            'task_type': task_type,
            'optimizations': self._extract_optimizations(response)
        }

    def _build_performance_prompt(
        self,
        task_type: str,
        code: str,
        metrics: Dict[str, Any],
        system: str,
        context: Dict[str, Any]
    ) -> str:
        """Build the prompt for performance task."""

        if task_type == 'ANALYZE':
            return f"""
I need you to perform comprehensive performance analysis.

{f"Code:\n```\n{code}\n```\n" if code else ""}

System:
{system}

{f"Current Metrics:\n{metrics}\n" if metrics else ""}

Please analyze:

1. **Time Complexity Analysis** ⏱️
   - Algorithm complexity (Big O)
   - Loop analysis
   - Recursive calls
   - Nested operations

2. **Space Complexity** 💾
   - Memory usage
   - Data structures efficiency
   - Memory leaks potential

3. **Database Performance** 🗄️
   - Query efficiency
   - N+1 query problems
   - Missing indexes
   - Connection pooling

4. **I/O Operations** 📁
   - File operations
   - Network calls
   - Blocking operations
   - Async opportunities

5. **Caching Opportunities** 🚀
   - What can be cached
   - Cache strategy
   - Cache invalidation

6. **Bottlenecks Identified** 🚧
   - CPU bottlenecks
   - Memory bottlenecks
   - I/O bottlenecks
   - Network bottlenecks

7. **Performance Score**: X/10

8. **Quick Wins**: Easy optimizations with high impact

Context: {context if context else 'None'}
"""

        elif task_type == 'OPTIMIZE':
            return f"""
I need you to optimize this code for performance.

Code:
```
{code}
```

System:
{system}

{f"Current Metrics:\n{metrics}\n" if metrics else ""}

Please provide:

1. **Optimized Code** ✨
   - Improved version
   - Comments explaining changes
   - Performance gains expected

2. **Optimization Techniques Applied** 🔧
   - Algorithm improvements
   - Data structure changes
   - Caching strategies
   - Query optimization
   - Parallel processing

3. **Before/After Comparison** 📊
   - Time complexity: O(?) → O(?)
   - Space complexity: O(?) → O(?)
   - Expected speedup: Xx faster

4. **Trade-offs** ⚖️
   - Code complexity
   - Memory usage
   - Maintainability

5. **Further Optimizations** 💡
   - Additional improvements possible
   - When to apply them
   - Cost/benefit analysis

Context: {context if context else 'None'}
"""

        elif task_type == 'LOAD_TEST':
            return f"""
I need you to create a load testing plan.

System:
{system}

{f"Current Metrics:\n{metrics}\n" if metrics else ""}

Please provide:

1. **Load Testing Strategy** 🎯
   - Test objectives
   - Success criteria
   - Load patterns to test

2. **Test Scenarios** 📋
   - Baseline test
   - Stress test
   - Spike test
   - Soak test
   - Scalability test

3. **Test Parameters** ⚙️
   - Concurrent users
   - Request rate
   - Test duration
   - Ramp-up strategy

4. **Metrics to Monitor** 📊
   - Response time (p50, p95, p99)
   - Throughput
   - Error rate
   - Resource utilization (CPU, Memory, Disk, Network)

5. **Expected Results** 🎲
   - Performance baselines
   - Breaking points
   - Bottlenecks to watch

6. **Tools & Scripts** 🛠️
   - Recommended tools (JMeter, k6, Locust)
   - Test scripts
   - Monitoring setup

Context: {context if context else 'None'}
"""

        elif task_type == 'SCALE':
            return f"""
I need a scalability assessment and recommendations.

System:
{system}

{f"Current Metrics:\n{metrics}\n" if metrics else ""}

Please provide:

1. **Current State Assessment** 📊
   - Current capacity
   - Performance limits
   - Bottlenecks

2. **Scalability Analysis** 📈
   - Vertical scaling options
   - Horizontal scaling options
   - Database scaling
   - Caching strategies

3. **Scaling Strategy** 🎯
   - Short-term improvements
   - Long-term architecture
   - Migration path

4. **Architecture Recommendations** 🏗️
   - Microservices considerations
   - Load balancing
   - Database sharding
   - Caching layers
   - CDN usage
   - Async processing

5. **Cost Analysis** 💰
   - Infrastructure costs
   - Development effort
   - Maintenance costs
   - ROI estimation

6. **Implementation Roadmap** 🗺️
   - Phase 1: Quick wins
   - Phase 2: Medium-term improvements
   - Phase 3: Long-term scaling

Context: {context if context else 'None'}
"""

        elif task_type == 'PROFILE':
            return f"""
I need help with performance profiling.

{f"Code:\n```\n{code}\n```\n" if code else ""}

System:
{system}

{f"Current Metrics:\n{metrics}\n" if metrics else ""}

Please provide:

1. **Profiling Strategy** 🔍
   - What to profile
   - Profiling tools to use
   - Profiling duration

2. **Hot Paths** 🔥
   - Most frequently executed code
   - Expensive operations
   - Time-consuming functions

3. **Resource Usage** 💻
   - CPU usage patterns
   - Memory allocation
   - I/O operations
   - Network calls

4. **Optimization Priorities** 📋
   - High impact, low effort
   - High impact, high effort
   - Low impact items

5. **Profiling Tools** 🛠️
   - Recommended profilers
   - How to use them
   - Interpreting results

6. **Action Items** ✅
   - Immediate actions
   - Short-term improvements
   - Long-term optimizations

Context: {context if context else 'None'}
"""

        else:
            return system or code

    def _extract_optimizations(self, response: str) -> List[Dict[str, Any]]:
        """Extract optimization recommendations from response."""
        optimizations = []
        current_opt = {}

        lines = response.split('\n')
        for line in lines:
            line = line.strip()

            if line.startswith('**') and 'Optimization' in line:
                if current_opt:
                    optimizations.append(current_opt)
                current_opt = {'title': line.strip('*').strip()}
            elif 'Impact:' in line:
                current_opt['impact'] = line.split('Impact:')[-1].strip()
            elif 'Effort:' in line:
                current_opt['effort'] = line.split('Effort:')[-1].strip()

        if current_opt:
            optimizations.append(current_opt)

        return optimizations
